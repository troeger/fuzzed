#include "SimulationProxy.h"
#include "implementation/PetriNetSimulation.h"

#include "serialization/PNMLDocument.h"
#include "events/TopLevelEvent.h"
#include "FaultTreeConversion.h"

#include "util.h"
#include "xmlutil.h"
#include "Config.h"
#include "Constants.h"
#include "CommandLineParser.h"
#include "FatalException.h"

#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/foreach.hpp>
#include <boost/range/counting_range.hpp>

#include <map>
#include <set>
#include <iostream>
#include <fstream>
#include "DeadlockMonitor.h"
#include "FuzzTreeToFaultTree.h"
#include "resultxml.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

SimulationProxy::SimulationProxy(int argc, char** arguments) :
	m_numRounds(DEFAULT_SIMULATION_ROUNDS),
	m_convergenceThresh(0.000005),
	m_simulationTime(DEFAULT_SIMULATION_TIME)
{
	parseCommandline_default(argc, arguments);
}

SimulationResult SimulationProxy::runSimulationInternal(
	const boost::filesystem::path& inPath, const std::string modelId, const std::string resultId) 
{
	Simulation* sim = new PetriNetSimulation(
		modelId,
		resultId,
		inPath,
		m_simulationTime,
		m_missionTime,
		m_numRounds,
		m_convergenceThresh,
		true);
	SimulationResult res(modelId, resultId, util::timeStamp());
	
	try
	{
		std::function<void()> fun = [&]() { sim->run(); };
		DeadlockMonitor monitor(&fun);
		monitor.executeWithin(10000);
        res = (static_cast<PetriNetSimulation*>(sim))->result();
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

SimulationResult SimulationProxy::simulateFaultTree(
	const std::shared_ptr<TopLevelEvent> ft,
	const std::string modelId,
	const std::string resultId,
	const boost::filesystem::path& workingDir,
	std::ofstream* logfile)
{
	std::shared_ptr<PNDocument> doc;

	m_missionTime = ft->getMissionTime();
	if (m_missionTime <= 1)
		std::cout 
			<< "Warning: Components are assumed to fail one at the time."
			<< "For a very short mission time, possible failures may never occur." 
			<< std::endl;

	doc = std::shared_ptr<PNMLDocument>(new PNMLDocument());
	ft->serializePTNet(doc);

	const std::string petriNetFile = 
		workingDir.generic_string() + "petrinet" +  PNML::PNML_EXT;

	if (!doc->save(petriNetFile))
	{
		std::string err = std::string("Could not save petri net file: ") + petriNetFile;
		*logfile << err;
		throw FatalException(err);
	}

	return runSimulationInternal(petriNetFile, modelId, resultId);
}

void SimulationProxy::simulateAllConfigurations(
	const fs::path& inputFile,
	const fs::path& outputFile,
	const fs::path& workingDir,
	const fs::path& logFile)
{
	const auto inFile = inputFile.generic_string();
	ifstream file(inFile, ios::in | ios::binary);
	if (!file.is_open())
		throw runtime_error("Could not open file");

	std::ofstream* logFileStream = new std::ofstream(logFile.generic_string());
	
	try
	{
		std::vector<SimulationResult> results;
		std::set<Issue> issues;
		Model m(inFile);
		ResultsXML xml;

		const unsigned int decompositionNumber = m.getDecompositionNumber();
		const unsigned int missionTime = m.getMissionTime();
		const std::string modelId = m.getId();

		if (m.getType() == modeltype::FUZZTREE)
		{
			FuzzTreeToFaultTree transform(&m);
			const auto configs = transform.generateConfigurations();
			for (const FuzzTreeConfiguration& inst : configs)
			{
				Model faultTree = transform.faultTreeFromConfiguration(inst);
				const auto res = simulateFaultTree(fromGraphModel(faultTree), modelId, inst.getId(), workingDir, logFileStream);
				results.emplace_back(modelId, inst.getId(), util::timeStamp(), res);
			}

			xml.generate(configs, results, issues, std::ofstream(outputFile.generic_string()));
		}
		else
		{
			const auto res = simulateFaultTree(fromGraphModel(m), modelId, "", workingDir, logFileStream);
			results.emplace_back(modelId, "", util::timeStamp(), res);
			xml.generate(results, issues, std::ofstream(outputFile.generic_string()));
		}
	}
	catch (std::exception& e)
	{
		std::cout << e.what();
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
		parser.getLogFilePath());
}