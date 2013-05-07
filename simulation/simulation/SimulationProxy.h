#pragma once

#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <string>
#include <boost/filesystem/path.hpp>
#include <boost/program_options.hpp>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

#include "Config.h"
#include "platform.h"

using namespace std;

enum SimulationImpl
{
	TIMENET,
	DEFAULT
};


/************************************************************************/
/* SIMULATION LIBRARY                                                   */
/************************************************************************/
extern "C"
{
	void FT_DLL_API runSimulation(
		char* filePath, /* path to fault tree file */
		int missionTime,
		int numRounds,	/* the max number of simulation rounds. if convergence is specified, the actual number may be lower*/
		double convergenceThreshold, /* stop after reliability changes no more than this threshold */
		int maxTime		/* maximum duration of simulation in milliseconds */
		) noexcept;
}

/************************************************************************/
/* SIMLATION EXECUTABLE													*/
/* determines the simulation configuration from command line arguments, */
/* and runs the simulation												*/
/************************************************************************/

class SimulationProxy
{
public:
	// constructor for command line tool
	SimulationProxy(int numArguments, char** arguments);

	// constructor for library calls
	SimulationProxy(
		int missionTime,
		int numRounds,
		double convergenceThreshold,
		int maxTime);

	virtual ~SimulationProxy() {};

	// simulates all configurations from one file
	void simulateFile(const boost::filesystem::path& p, bool simulatePetriNet);

protected:
	void parseTimeNET(int numArguments, char** arguments);
	void parseStandard(int numArguments, char** arguments);

	bool runSimulation(
		const boost::filesystem::path& p, 
		SimulationImpl implementationType,
		void* additionalArguments = NULL);
	
	int m_missionTime;
	int m_simulationTime;
	int m_numRounds;
	int m_numAdaptiveRounds;
	double m_convergenceThresh;

	bool m_bSimulateUntilFailure;

	boost::program_options::options_description m_timeNetOptions;
	boost::program_options::options_description m_standardOptions;
	
	static bool acceptFileExtension(const boost::filesystem::path& p);
};
