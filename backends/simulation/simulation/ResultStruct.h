#pragma once

// a simple data structure for the results computed during Fault Tree Simulation
struct SimulationResultStruct
{
	SimulationResultStruct() : 
		reliability(1.0), meanAvailability(1.0), mttf(-1.0), nRounds(0), nFailures(0), duration(0.0) {};

	double reliability;
	double meanAvailability;
	double mttf;
	unsigned int nRounds;
	unsigned int nFailures;
	double duration;

	const bool isValid() { return nRounds > 0; }
};
