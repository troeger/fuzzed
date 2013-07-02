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

namespace faulttree
{
	class FaultTree;
}

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
	void /*FT_DLL_API*/ runSimulationOnFile(
		char* filePath, /* path to fault tree file */
		int missionTime,
		int numRounds,	/* the max number of simulation rounds. if convergence is specified, the actual number may be lower*/
		double convergenceThreshold, /* stop after reliability changes no more than this threshold */
		int maxTime		/* maximum duration of simulation in milliseconds */
		) noexcept;

	void /*FT_DLL_API*/ runSimulation(
		char* fuzztreeXML, /* fuzztree XML */
		int missionTime,
		int numRounds,	/* the max number of simulation rounds. if convergence is specified, the actual number may be lower*/
		double convergenceThreshold, /* stop after reliability changes no more than this threshold */
		int maxTime		/* maximum duration of simulation in milliseconds */
		) noexcept; // TODO
}

class TimeNETProperties;

class SimulationProxy
{
public:
	// constructor for command line tool
	SimulationProxy(int numArguments, char** arguments);

	// constructor for library calls
	SimulationProxy(
		unsigned int missionTime,
		unsigned int numRounds,
		double convergenceThreshold,
		unsigned int maxTime);

	virtual ~SimulationProxy();;

	// simulates all configurations from one file
	void simulateFile(const boost::filesystem::path& p, SimulationImpl impl, bool simulatePetriNet);
	
protected:
	void parseStandard(int numArguments, char** arguments);

	bool runSimulationInternal(
		const boost::filesystem::path& p, 
		SimulationImpl implementationType,
		void* additionalArguments = NULL);
	
	unsigned int m_missionTime;
	unsigned int m_simulationTime;
	unsigned int m_numRounds;
	unsigned int m_numAdaptiveRounds;
	double m_convergenceThresh;

	bool m_bSimulateUntilFailure;

	boost::program_options::options_description m_options;
	
	static bool acceptFileExtension(const boost::filesystem::path& p);

	TimeNETProperties* m_timeNetProperties;
};
