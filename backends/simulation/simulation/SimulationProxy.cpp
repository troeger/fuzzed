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

namespace po = boost::program_options;
namespace fs = boost::filesystem;

SimulationProxy::SimulationProxy(int argc, char** arguments) :
	m_numRounds(DEFAULT_SIMULATION_ROUNDS),
	m_convergenceThresh(0.000005),
	m_simulationTime(DEFAULT_SIMULATION_TIME)
{
	parseCommandline_default(argc, arguments);
}

SimulationResultStruct SimulationProxy::runSimulationInternal(
	const boost::filesystem::path& petriNetFile) 
{
	Simulation* sim = new PetriNetSimulation(
		petriNetFile,
		m_simulationTime,
		m_missionTime,
		m_numRounds,
		m_convergenceThresh,
		true);
	SimulationResultStruct res;
	
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

SimulationResultStruct SimulationProxy::simulateFaultTree(
	const std::shared_ptr<TopLevelEvent> ft,
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

	return runSimulationInternal(petriNetFile);
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
		// TODO: Rewrite the actual simulation call

		// TODO: Log errors
		
		// TODO: Output results
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