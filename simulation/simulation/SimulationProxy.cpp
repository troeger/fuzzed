#include "SimulationProxy.h"
#include "implementation/TimeNETSimulation.h"
#include "implementation/PetriNetSimulation.h"

#include "serialization/PNMLDocument.h"
#include "serialization/TNDocument.h"
#include "events/TopLevelEvent.h"
#include "FaultTreeImport.h"
#include "FuzzTreeTransform.h"
#include "FaultTreeConversion.h"

#include "util.h"
#include "Config.h"
#include "Constants.h"
#include <omp.h>

#include "faulttree.h"
#include "fuzztree.h"

#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/foreach.hpp>
#include <boost/range/counting_range.hpp>

#include <map>
#include <set>
#include <iostream>
#include <fstream>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

namespace po = boost::program_options;
namespace fs = boost::filesystem;

SimulationProxy::SimulationProxy(int argc, char** arguments) :
	m_numRounds(0),
	m_convergenceThresh(0.0),
	m_simulationTime(0),
	m_bSimulateUntilFailure(true),
	m_numAdaptiveRounds(0),
	m_timeNetProperties(nullptr)
{
	try
	{
		parseCommandline(argc, arguments);
	}
	catch (const exception& e)
	{
		cout << "Exception when invoking simulation: " << e.what();
	}
	catch (...)
	{
		cout << "Unknown exception when invoking simulation";
	}
}

SimulationProxy::SimulationProxy(unsigned int numRounds, double convergenceThreshold, unsigned int maxTime) : 
	m_numRounds(numRounds),
	m_convergenceThresh(convergenceThreshold),
	m_simulationTime(maxTime),
	m_bSimulateUntilFailure(true),
	m_numAdaptiveRounds(0),
	m_timeNetProperties(nullptr)
{}

bool SimulationProxy::runSimulationInternal(const fs::path& p, SimulationImpl implementationType, void* additionalArguments) 
{
	Simulation* sim;
	switch (implementationType)
	{
	case TIMENET:
		{
			assert(additionalArguments != nullptr);
			sim = new TimeNETSimulation(p, m_simulationTime, m_missionTime, m_numRounds, additionalArguments);
			break;
		}
	case DEFAULT:
		{
			std::string fileName = p.generic_string();
			std::string logFileName = fileName;
			util::replaceFileExtensionInPlace(logFileName, "");

			sim = new PetriNetSimulation(
				fileName, 
				logFileName, 
				m_simulationTime, 
				m_missionTime, 
				m_numRounds,
				m_convergenceThresh,
				m_bSimulateUntilFailure,
				m_numAdaptiveRounds);

			break;
		}
	default:
		{
			assert(false);
			return false;
		}
	}
	
	bool success = false;
	try
	{
// uncomment to do one simulation run for all possible numbers of threads
// #define MEASURE_SPEEDUP true
#ifdef MEASURE_SPEEDUP
		for (int i : boost::counting_range(1, omp_get_max_threads()))
		{
			omp_set_num_threads(i);
			cout << "*** " << i << "THREADS ***" << endl;
			success &= sim->run(false);
		}
#else
		success = sim->run();
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
	return success;
}

void SimulationProxy::parseCommandline(int numArguments, char** arguments)
{
	string directoryName, filePath;
	bool simulatePetriNet;
	bool useTimeNET;
	unsigned int numAdaptiveRounds; // not yet implemented
	int confidence;
	float epsilon;

	m_options.add_options()
		("help,h", "produce help message")
		("TN",			po::value<bool>(&useTimeNET)->default_value(false),									"Use TimeNET simulation")
		("PN",			po::value<bool>(&simulatePetriNet)->default_value(false),							"Simulate Petri Net directly")
		("file,f",		po::value<string>(&filePath),														"Path to FuzzTree or PNML file")
		("dir,d",		po::value<string>(&directoryName),													"Directory containing FuzzTree or PNML files")
		("time,t",		po::value<unsigned int>(&m_simulationTime)->default_value(DEFAULT_SIMULATION_TIME),	"Maximum Simulation Time in milliseconds")
		("steps,s",		po::value<unsigned int>(&m_missionTime)->default_value(DEFAULT_SIMULATION_STEPS),	"Number of Simulation Steps")
		("rounds,r",	po::value<unsigned int>(&m_numRounds)->default_value(DEFAULT_SIMULATION_ROUNDS),	"Number of Simulation Rounds")
		("conf",		po::value<int>(&confidence)->default_value(DEFAULT_CONFIDENCE),						"Confidence level (TimeNET only)")
		("epsilon,e",	po::value<float>(&epsilon)->default_value(DEFAULT_EPSILON),							"Epsilon (TimeNET only)")
		("MTTF",		po::value<bool>(&m_bSimulateUntilFailure)->default_value(true),						"Simulate each Round until System Failure, necessary for MTTF")
		("converge,c",	po::value<double>(&m_convergenceThresh)->default_value((double)0.0000),				"Cancel simulation after the resulting reliability differs in less than this threshold")
		("adaptive,a",	po::value<unsigned int>(&numAdaptiveRounds)->default_value(0),						"Adaptively adjust the number of Simulation Rounds, NOT YET IMPLEMENTED");

	po::variables_map optionsMap;
	po::store(po::parse_command_line(numArguments, arguments, m_options), optionsMap);
	po::notify(optionsMap);

	if (optionsMap.count("help")) 
	{
		cout << m_options << endl;
		return;
	}

	if (useTimeNET)
	{
		m_timeNetProperties = new TimeNETProperties();
		m_timeNetProperties->filePath = filePath;
		m_timeNetProperties->seed = rand();
		m_timeNetProperties->confLevel = confidence;
		m_timeNetProperties->epsilon = epsilon;
		m_timeNetProperties->maxExecutionTime = m_simulationTime;
		m_timeNetProperties->transientSimTime = m_missionTime;
	}

	const bool bDir = optionsMap.count("dir") > 0;
	const bool bFile = optionsMap.count("file") > 0;
	if (!bDir && !bFile)
	{
		cout << "Please specify either a directory or a file" << endl;
		cout << m_options << endl;
		return;
	}

	if (bDir)
	{
		const auto dirPath = fs::path(directoryName.c_str());
		if (!is_directory(dirPath))
			throw runtime_error("Not a directory: " + directoryName);

		cout << "Simulating all files in directory " << dirPath.generic_string() << endl;
		fs::directory_iterator it(dirPath), eod;
		BOOST_FOREACH(fs::path const &p, std::make_pair(it, eod))   
		{
			if (is_regular_file(p) && acceptFileExtension(p))
				simulateFile(p, useTimeNET ? TIMENET : DEFAULT, simulatePetriNet);
		}
	}
	else if (bFile)
	{
		const auto fPath = fs::path(filePath.c_str());
		if (!is_regular_file(fPath))
			throw runtime_error("Not a file: " + filePath);

		simulateFile(fPath, useTimeNET ? TIMENET : DEFAULT/*STRUCTUREFORMULA_ONLY*/, simulatePetriNet);
	}
}

void SimulationProxy::simulateFile(const fs::path& p, SimulationImpl impl, bool simulatePetriNet)
{	
	cout << "Simulating..." << endl;
	
	assert(is_regular_file(p) && acceptFileExtension(p));

	const auto ext = p.extension();
	if (((ext == PNML::PNML_EXT && impl == DEFAULT) || (ext == timeNET::TN_EXT)) && simulatePetriNet)
		runSimulationInternal(p, impl); // run simulation directly

	else if (ext == fuzzTree::FUZZ_TREE_EXT)
		simulateAllConfigurations(p, impl);

	else if (ext == faultTree::FAULT_TREE_EXT)
	{
		ifstream file(p.generic_string(), ios::in | ios::binary);
		if (!file.is_open()) throw runtime_error("Could not open file");

		const auto simTree = faulttree::faultTree(file, xml_schema::Flags::dont_validate);
		std::shared_ptr<TopLevelEvent> ft = fromGeneratedFaultTree(simTree->topEvent()); 
		ft->print(cout);

		string newFileName = p.generic_string();
		util::replaceFileExtensionInPlace(newFileName, (impl == DEFAULT) ? PNML::PNML_EXT : timeNET::TN_EXT);
		simulateFaultTree(ft, newFileName, impl);
	}
}

bool SimulationProxy::acceptFileExtension(const boost::filesystem::path& p)
{
	return
		p.extension() == PNML::PNML_EXT ||
		p.extension() == fuzzTree::FUZZ_TREE_EXT ||
		p.extension() == faultTree::FAULT_TREE_EXT ||
		p.extension() == timeNET::TN_EXT;
}

void SimulationProxy::simulateFaultTree(std::shared_ptr<TopLevelEvent> ft, const std::string& newFileName, SimulationImpl impl)
{
	std::shared_ptr<PNDocument> doc;

	m_missionTime = ft->getMissionTime();

	switch (impl)
	{
	case DEFAULT:
		doc = std::shared_ptr<PNMLDocument>(new PNMLDocument());
		ft->serializePTNet(doc);
		break;
	case TIMENET:
	case STRUCTUREFORMULA_ONLY:
		auto TNdoc = std::shared_ptr<TNDocument>(new TNDocument());
		ft->serializeTimeNet(TNdoc);
		std::cout << ft->serializeAsFormula(TNdoc) << endl;
		doc = TNdoc;
		break;
	}

	if (impl == STRUCTUREFORMULA_ONLY)
		return;

	doc->save(newFileName);	
	runSimulationInternal(newFileName, impl, m_timeNetProperties);
}

void SimulationProxy::simulateAllConfigurations(const fs::path &p, SimulationImpl impl)
{
	ifstream file(p.generic_string(), ios::in | ios::binary);
	if (!file.is_open()) throw runtime_error("Could not open file");

	FuzzTreeTransform ftTransform(file);
	int i = 0;
	for (const auto& ft : ftTransform.transform())
	{
		std::shared_ptr<TopLevelEvent> simTree = fromGeneratedFaultTree(ft.topEvent()); 
		std::string newFileName = p.generic_string();
		util::replaceFileExtensionInPlace(newFileName, util::toString(++i) + ((impl == DEFAULT) ? PNML::PNML_EXT : timeNET::TN_EXT));
		simTree->print(cout);
		simulateFaultTree(simTree, newFileName, impl);
	}
}
