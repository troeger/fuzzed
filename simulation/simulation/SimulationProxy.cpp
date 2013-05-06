#include "SimulationProxy.h"
#include "implementation/TimeNETSimulation.h"
#include "implementation/PetriNetSimulation.h"

#include "serialization/PNMLDocument.h"
#include "FaultTreeNode.h"
#include "FaultTreeImport.h"
#include "FuzzTreeTransform.h"

#include "util.h"
#include "Config.h"
#include "Constants.h"
#include <omp.h>

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
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

namespace po = boost::program_options;
namespace fs = boost::filesystem;

SimulationProxy::SimulationProxy(int argc, char** arguments)
{
	try
	{
		bool useTimeNET = false;
		for (int i : boost::counting_range(1, argc))
		{
			if (string(arguments[i]) == "TimeNET")
				useTimeNET = true;
		}
		
		useTimeNET ? parseTimeNET(argc, arguments) : parseStandard(argc, arguments);
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

bool SimulationProxy::runSimulation(const fs::path& p, SimulationImpl implementationType, void* additionalArguments) 
{
	Simulation* sim;
	switch (implementationType)
	{
	case TIMENET:
		{
			assert(additionalArguments != nullptr);
			sim = new TimeNETSimulation(p, m_simulationTime, m_simulationSteps, m_numRounds, additionalArguments);
			break;
		}
	case DEFAULT:
		{
			std::string fileName = p.generic_string();
			std::string logFileName = fileName;
			util::replaceFileExtensionInPlace(logFileName, ".log");

			sim = new PetriNetSimulation(
				fileName, 
				logFileName, 
				m_simulationTime, 
				m_simulationSteps, 
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

	delete sim;
	return success;
}

void SimulationProxy::parseStandard(int numArguments, char** arguments)
{
	string directoryName, filePath;
	bool simulatePetriNet;
	int numAdaptiveRounds; // not yet implemented
	
	m_standardOptions.add_options()
		("help,h", "produce help message")
		("PN",			po::value<bool>(&simulatePetriNet)->default_value(false),					"Simulate Petri Net directly")
		("file,f",		po::value<string>(&filePath),												"Path to FuzzTree or PNML file")
		("dir,d",		po::value<string>(&directoryName),											"Directory containing FuzzTree or PNML files")
		("time,t",		po::value<int>(&m_simulationTime)->default_value(DEFAULT_SIMULATION_TIME),	"Maximum Simulation Time in milliseconds")
		("steps,s",		po::value<int>(&m_simulationSteps)->default_value(DEFAULT_SIMULATION_STEPS),"Number of Simulation Steps")
		("rounds,r",	po::value<int>(&m_numRounds)->default_value(DEFAULT_SIMULATION_ROUNDS),		"Number of Simulation Rounds")
		("MTTF",		po::value<bool>(&m_bSimulateUntilFailure)->default_value(true),				"Simulate each Round until System Failure, necessary for MTTF")
		("converge,c",	po::value<double>(&m_convergenceThresh)->default_value((double)0.0001),		"Cancel simulation after the resulting reliability differs in less than this threshold")
		("adaptive,a",	po::value<int>(&numAdaptiveRounds)->default_value(0),						"Adaptively adjust the number of Simulation Rounds, NOT YET IMPLEMENTED");

	po::variables_map optionsMap;
	po::store(po::parse_command_line(numArguments, arguments, m_standardOptions), optionsMap);
	po::notify(optionsMap);

	if (optionsMap.count("help")) 
	{
		cout << m_standardOptions << endl;
		return;
	}

	const bool bDir = optionsMap.count("dir") > 0;
	const bool bFile = optionsMap.count("file") > 0;
	if (!bDir && !bFile)
	{
		cout << "Please specify either a directory or a file" << endl;
		cout << m_standardOptions << endl;
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
				simulateFile(p, simulatePetriNet);
		}
	}
	else if (bFile)
	{
		const auto fPath = fs::path(filePath.c_str());
		if (!is_regular_file(fPath))
			throw runtime_error("Not a file: " + filePath);

		simulateFile(fPath, simulatePetriNet);
	}
}

void SimulationProxy::parseTimeNET(int numArguments, char** arguments)
{
	string fileName			= DEFAULT_FILE_PATH;
	string directoryName	= DEFAULT_FILE_PATH;
	string integrationPath	= DEFAULT_INTEGRATION_PROPS_PATH;
	string logsPath			= DEFAULT_LOG_PROPS_PATH;
	string timeNetPath		= DEFAULT_TIMENET_PATH;
	int simulationTime		= DEFAULT_SIMULATION_TIME;

	m_timeNetOptions.add_options()
		("help", "produce help message")
		("TimeNET", "Simulate with TimeNET")
		("file,f",		po::value<string>(&fileName),			"Name of Petri Net File in TimeNET XML format")
		("time,t",		po::value<int>(&simulationTime),		"Simulation Time in milliseconds")
		("iProps,i",	po::value<string>(&integrationPath),	"Path to integration.props")
		("lProps,l",	po::value<string>(&logsPath),			"Path to log4j.props")
		("TNjar",		po::value<string>(&timeNetPath),		"Path to TimeNET.jar");

	po::variables_map timeNETMap;
	po::store(po::parse_command_line(numArguments, arguments, m_timeNetOptions), timeNETMap);
	po::notify(timeNETMap);

	if (timeNETMap.count("help")) 
	{
		cout << m_timeNetOptions << "\n";
		return;
	}

	TimeNETProperties* props = new TimeNETProperties;
	props->integrationPropsPath = integrationPath;
	props->logPropsPath = logsPath;
	props->simulationServerPath = timeNetPath;

	props->serverIP = "localhost";
	props->resultIP = "localhost";
	props->resultPort = 4455;
	props->serverPort = 4455;

	assert(!fileName.empty());

	runSimulation(fs::path(fileName), TIMENET, (void*)props);
	delete props;
}

void SimulationProxy::simulateFile(const fs::path& p, bool simulatePetriNet)
{	
	assert(is_regular_file(p) && acceptFileExtension(p));

	if (p.extension() == PNML::PNML_EXT && simulatePetriNet)
		runSimulation(p, DEFAULT); // run simulation directly

	else if (p.extension() == fuzzTree::FUZZ_TREE_EXT)
	{ // transform into fault trees first
		fs::path targetDir = p;
		string name = util::fileNameFromPath(p.generic_string(), false);
		util::replaceFileExtensionInPlace(name, "");
		targetDir.remove_filename();
		targetDir /= "faultTrees_" + name;

		if (!fs::create_directory(targetDir) && !fs::is_directory(targetDir))
			throw runtime_error("Could not create directory: " + targetDir.generic_string());

		FuzzTreeTransform::transformFuzzTree(p.generic_string(), targetDir.generic_string());
		fs::directory_iterator it(targetDir), eod;
		BOOST_FOREACH(fs::path const &p, std::make_pair(it, eod))
		{
			if (fs::is_regular_file(p) && p.extension() == faultTree::FAULT_TREE_EXT)
				simulateFile(p, false);
		}
	}

	else if (p.extension() == faultTree::FAULT_TREE_EXT)
	{ // already a fault tree
		FaultTreeNode* ft = FaultTreeImport::loadFaultTree(p.generic_string());
		if (!ft || !ft->isValid()) throw("Invalid Fault Tree");
		
		ft->print(cout);

		string newFileName = p.generic_string();
		util::replaceFileExtensionInPlace(newFileName, PNML::PNML_EXT);

		boost::shared_ptr<PNMLDocument> doc = 
			boost::shared_ptr<PNMLDocument>(new PNMLDocument());
		ft->serialize(doc);
		delete ft;

		doc->save(newFileName);
		runSimulation(newFileName, DEFAULT);
	}		
}

bool SimulationProxy::acceptFileExtension(const boost::filesystem::path& p)
{
	return
		p.extension() == PNML::PNML_EXT ||
		p.extension() == fuzzTree::FUZZ_TREE_EXT ||
		p.extension() == faultTree::FAULT_TREE_EXT;
}

void runSimulation(
	char* filePath, /* path to fault tree file */ 
	int missionTime, 
	int numRounds, /* the max number of simulation rounds. if convergence is specified, the actual number may be lower*/ 
	double convergenceThreshold, /* stop after reliability changes no more than this threshold */
	int maxTime /* maximum duration of simulation in milliseconds */) noexcept
{
	PetriNetSimulation* sim = nullptr;
	FaultTreeNode* ft = nullptr;
	
	try
	{
		string newFileName(filePath);
		ft = FaultTreeImport::loadFaultTree(newFileName);
		if (!ft || !ft->isValid())
		{
			cout << "Invalid Fault Tree! " << endl;
			return;
		}

		util::replaceFileExtensionInPlace(newFileName, ".pnml");
		boost::shared_ptr<PNMLDocument> doc = 
			boost::shared_ptr<PNMLDocument>(new PNMLDocument());

		ft->serialize(doc);
		ft->print(cout);
		
		doc->save(newFileName); // save PNML file

		std::string logFileName = newFileName;
		util::replaceFileExtensionInPlace(logFileName, ".log");

		sim = new PetriNetSimulation(
			newFileName, 
			logFileName, 
			maxTime, 
			missionTime, 
			numRounds,
			convergenceThreshold,
			true, /* simulate until failure for MTTF */
			0 /* not yet implemented */);

		sim->run();
	}
	catch (const exception& e)
	{
		cout << "Unhandled Exception during Simulation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Exception during Simulation" << endl;
	}
	
	delete ft;
	delete sim;
}