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

class FaultTreeNode;

enum SimulationImpl
{
	TIMENET,
	DEFAULT,
	STRUCTUREFORMULA_ONLY
};
 
struct TimeNETProperties;

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

	// triggers a faulttree simulation on a fuzztree or faulttree file
	void simulateFile(const boost::filesystem::path& p, SimulationImpl impl, bool simulatePetriNet);

	// simulates all configurations from one file
	void simulateAllConfigurations(const boost::filesystem::path&p, SimulationImpl impl);

	void simulateFaultTree(std::shared_ptr<FaultTreeNode> ft, const std::string& newFileName, SimulationImpl impl);

protected:
	void parseCommandline(int numArguments, char** arguments);
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

	TimeNETProperties* m_timeNetProperties; // ownership usually transferred to Simulation. Do NOT call delete on it. -.-
};
