#include "SimulationProxy.h"
#include "implementation/TimeNETSimulation.h"
#include "implementation/PetriNetSimulation.h"

#include "serialization/PNMLDocument.h"
#include "serialization/TNDocument.h"
#include "events/TopLevelEvent.h"
#include "FuzzTreeTransform.h"
#include "FaultTreeConversion.h"

#include "util.h"
#include "xmlutil.h"
#include "Config.h"
#include "Constants.h"
#include "CommandLineParser.h"
#include "FatalException.h"

#if defined(MEASURE_SPEEDUP)
#include <omp.h>
#endif
// Generated files...
#include "faulttree.h"
#include "fuzztree.h"
#include "simulationResult.h"

#include <xsd/cxx/xml/dom/serialization-header.hxx>

#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/foreach.hpp>
#include <boost/range/counting_range.hpp>

#include <map>
#include <set>
#include <iostream>
#include <fstream>

namespace po = boost::program_options;
namespace fs = boost::filesystem;

SimulationProxy::SimulationProxy(int argc, char** arguments) :
	m_numRounds(DEFAULT_SIMULATION_ROUNDS),
	m_convergenceThresh(0.000005),
	m_simulationTime(DEFAULT_SIMULATION_TIME),
	m_timeNetProperties(nullptr)
{
	parseCommandline_default(argc, arguments);
}

SimulationResultStruct SimulationProxy::runSimulationInternal(
	const boost::filesystem::path& petriNetFile,
	SimulationImpl implementationType,
	void* additionalArguments) 
{
	Simulation* sim = nullptr;
	SimulationResultStruct res;
	switch (implementationType)
	{
	case TIMENET:
		{
			assert(additionalArguments != nullptr);
			// TODO make this produce rubbish output only in workingDir
			sim = new TimeNETSimulation(petriNetFile, m_simulationTime, m_missionTime, m_numRounds, additionalArguments);
			break;
		}
	case DEFAULT:
		{
			sim = new PetriNetSimulation(
				petriNetFile,
				m_simulationTime, 
				m_missionTime, 
				m_numRounds,
				m_convergenceThresh,
				true);

			break;
		}
	default:
		assert(false);
		return res;
	}
	
	try
	{
#ifdef MEASURE_SPEEDUP
		for (int i : boost::counting_range(1, omp_get_max_threads()))
		{
			omp_set_num_threads(i);
//			cout << "*** " << i << "THREADS ***" << endl;
			sim->run();
		}
#else
		sim->run();
		if (implementationType == DEFAULT)
			res = (static_cast<PetriNetSimulation*>(sim))->result();
#endif
	}
	catch (exception& e)
	{
		cout << "Exception during simulation: " << e.what(); 
	}
	catch (...)
	{
		cout << "Unknown Exception during simulation";
	}
	
	delete sim;
	return res;
}

bool SimulationProxy::acceptFileExtension(const boost::filesystem::path& p)
{
	return
		p.extension() == PNML::PNML_EXT ||
		p.extension() == fuzzTree::FUZZ_TREE_EXT ||
		p.extension() == faultTree::FAULT_TREE_EXT ||
		p.extension() == timeNET::TN_EXT;
}

SimulationResultStruct SimulationProxy::simulateFaultTree(
	const std::shared_ptr<TopLevelEvent> ft,
	const boost::filesystem::path& workingDir,
	std::ofstream* logfile,
	SimulationImpl impl)
{
	std::shared_ptr<PNDocument> doc;

	m_missionTime = ft->getMissionTime();
	if (m_missionTime <= 1) // TODO: print simulation warning here!
		std::cout 
			<< "Warning: Components are assumed to fail one at the time."
			<< "For a very short mission time, possible failures may never occur." 
			<< std::endl;

	switch (impl)
	{
	case DEFAULT:
		doc = std::shared_ptr<PNMLDocument>(new PNMLDocument());
		ft->serializePTNet(doc);
		break;
	case TIMENET:
		m_timeNetProperties->maxExecutionTime = m_simulationTime;
		m_timeNetProperties->transientSimTime = m_missionTime;
	case STRUCTUREFORMULA_ONLY:
		auto TNdoc = std::shared_ptr<TNDocument>(new TNDocument());
		ft->serializeTimeNet(TNdoc);
		doc = TNdoc;
		break;
	}

	if (impl == STRUCTUREFORMULA_ONLY)
		return SimulationResultStruct();

	const std::string petriNetFile = 
		workingDir.generic_string() + "petrinet" + 
		std::string((impl == DEFAULT) ? PNML::PNML_EXT : timeNET::TN_EXT);

	if (!doc->save(petriNetFile))
	{
		std::string err = std::string("Could not save petri net file: ") + petriNetFile;
		*logfile << err;
		throw FatalException(err);
	}

	return runSimulationInternal(petriNetFile, impl, m_timeNetProperties);
}

void SimulationProxy::simulateAllConfigurations(
	const fs::path& inputFile,
	const fs::path& outputFile,
	const fs::path& workingDir,
	const fs::path& logFile,
	SimulationImpl impl)
{
	const auto inFile = inputFile.generic_string();
	ifstream file(inFile, ios::in | ios::binary);
	if (!file.is_open())
		throw runtime_error("Could not open file");

	std::ofstream* logFileStream = new std::ofstream(logFile.generic_string());
	simulationResults::SimulationResults simResults;

	try
	{
		std::set<Issue> issues;
		FuzzTreeTransform ftTransform(file, issues);
		if (!ftTransform.isValid())
		{
			const auto simTree = faulttree::faultTree(inputFile.generic_string(), xml_schema::Flags::dont_validate);
			const std::shared_ptr<TopLevelEvent> ft = fromGeneratedFaultTree(simTree->topEvent()); 
			if (ft)
			{ // in this case there is only a faulttree, so no configuration information will be serialized

				const SimulationResultStruct res = 
					simulateFaultTree(ft, workingDir, logFileStream, impl);

				simulationResults::Result r(
					ft->getId(),
					util::timeStamp(),
					ft->getCost(),
					res.reliability,
					res.nFailures,
					res.nRounds,
					res.isValid());

				r.availability(res.meanAvailability);
				r.duration(res.duration);
				r.mttf(res.mttf);
				
				simResults.result().push_back(r);
			}
			else
			{
				issues.insert(Issue::fatalIssue("Could not read fault tree. Problem during transformation."));
			}
		}
		else
		{
			for (const auto& ft : ftTransform.transform())
			{
				std::shared_ptr<TopLevelEvent> simTree = fromGeneratedFuzzTree(ft.second.topEvent());
				{
					const SimulationResultStruct res = 
						simulateFaultTree(simTree, workingDir, logFileStream, impl);

					// debug output
					// 			simTree->print(cout, 0);
					// 			fuzztree::fuzzTree(cout, ft.second);

					simulationResults::Result r(
						simTree->getId(),
						util::timeStamp(),
						simTree->getCost(),
						res.reliability,
						res.nFailures,
						res.nRounds,
						res.isValid());

					r.availability(res.meanAvailability);
					r.duration(res.duration);
					r.mttf(res.mttf);
					r.configuration(serializedConfiguration(ft.first));

					simResults.result().push_back(r);
				}
			}
		}
		// Log errors
		for (const Issue& issue : issues)
			simResults.issue().push_back(issue.serialized());

		std::ofstream output(outputFile.generic_string());
		simulationResults::simulationResults(output, simResults);
		output.close();
	}
	catch (std::exception& e)
	{
		*logFileStream << e.what() << std::endl;
	}
}

void SimulationProxy::parseCommandline_default(int numArguments, char** arguments)
{	
	CommandLineParser parser;
	parser.parseCommandline(numArguments, arguments);

	simulateAllConfigurations(
		parser.getInputFilePath(),
		parser.getOutputFilePath(),
		parser.getWorkingDirectory(),
		parser.getLogFilePath(),
		DEFAULT /*Simulation Implementation: custom*/);
}