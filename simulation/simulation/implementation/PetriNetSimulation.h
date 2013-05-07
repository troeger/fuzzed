#pragma once
#include "Simulation.h"

#include <fstream>

class PetriNet;

class PetriNetSimulation : public Simulation
{
public:
	PetriNetSimulation(
		const boost::filesystem::path& p,
		const std::string& outputFileName,
		int simulationTime,					// the maximum duration of one simulation in seconds
		int simulationSteps,				// the number of logical simulation steps performed in each round
		int numRounds,						// the number of simulation rounds performed in parallel
		double convergenceThresh,			// simulation stops after 
		bool simulateUntilFailure = true,	// if true, the simulation stops only with a SimulationException. necessary for MTTF computations
		int numAdaptiveRounds = 0);			// number of rounds performed to adapt OpenMP parallelization

	virtual bool run() override;

	void writeResultXML(
		const unsigned long& numFailures, 
		const unsigned long& count, 
		const long double& unreliability, 
		const long double& avgFailureTime_all, 
		const double& endTime, 
		const double& startTime, 
		const long double& meanAvailability);

	void printResults(
		const unsigned long& numFailures, 
		const unsigned long& count, 
		const long double& unreliability, 
		const long double& avgFailureTime_all, 
		const double& endTime, 
		const double& startTime, 
		const long double& meanAvailability);

	virtual ~PetriNetSimulation();

protected:
	// performs one round of m_numSimulationSteps discrete time steps
	SimulationResult runOneRound(PetriNet* net);

	// performs one single simulation step
	void simulationStep(PetriNet* pn, int tick);

	void tryTimedTransitions(PetriNet* pn, int tick);
	void tryImmediateTransitions(PetriNet* pn, int tick, bool& immediateOnly);

	std::string m_outputFileName;
	std::ofstream* m_outStream;
	std::ofstream* m_debugOutStream;

	const bool m_simulateUntilFailure;
	const int m_numAdaptiveRounds;
	double m_convergenceThresh;
};