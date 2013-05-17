#pragma once
#include "Simulation.h"
#include "ResultStruct.h"

#include <fstream>

class PetriNet;

class PetriNetSimulation : public Simulation
{
public:
	PetriNetSimulation(
		const boost::filesystem::path& p,
		const std::string& outputFileName,
		unsigned int simulationTime,		// the maximum duration of one simulation in seconds
		unsigned int simulationSteps,		// the number of logical simulation steps performed in each round
		unsigned int numRounds,				// the number of simulation rounds performed in parallel
		double convergenceThresh,			// simulation stops after 
		bool simulateUntilFailure = true,	// if true, the simulation stops only with a SimulationException. necessary for MTTF computations
		unsigned int numAdaptiveRounds = 0);			// number of rounds performed to adapt OpenMP parallelization

	virtual bool run() override;

	void writeResultXML(const SimulationResult& res);
	void printResults(const SimulationResult& res);

	virtual ~PetriNetSimulation();

protected:
	// performs one round of m_numSimulationSteps discrete time steps
	SimulationRoundResult runOneRound(PetriNet* net);

	// performs one single simulation step, returns whether the net is still valid
	bool simulationStep(PetriNet* pn, int tick);

	void tryTimedTransitions(PetriNet* pn, int tick);
	void tryImmediateTransitions(PetriNet* pn, int tick, bool& immediateOnly);

	std::string m_outputFileName;
	std::ofstream* m_outStream;
	std::ofstream* m_debugOutStream;

	const bool m_simulateUntilFailure;
	const int m_numAdaptiveRounds;
	double m_convergenceThresh;
};