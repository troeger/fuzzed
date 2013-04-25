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

using namespace std;

enum SimulationImpl
{
	TIMENET,
	DEFAULT
};

/************************************************************************/
/* determines the simulation configuration from command line arguments, */
/* and runs the simulation												*/
/************************************************************************/

class SimulationProxy
{
public:
	SimulationProxy(int numArguments, char** arguments);

	virtual ~SimulationProxy() {};

	void run();

protected:
	void parseTimeNET(int numArguments, char** arguments);
	void parseStandard(int numArguments, char** arguments);

	// simulates all configurations from one file
	void simulateFile(const boost::filesystem::path& p, bool simulatePetriNet);
	bool runSimulation(
		boost::filesystem::path p, 
		SimulationImpl implementationType,
		void* additionalArguments = NULL);
	
	int m_simulationSteps;
	int m_simulationTime;
	int m_numRounds;
	int m_numAdaptiveRounds;
	double m_convergenceThresh;

	bool m_bSimulateUntilFailure;

	boost::program_options::options_description m_timeNetOptions;
	boost::program_options::options_description m_standardOptions;
};