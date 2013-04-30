#pragma once
#include <assert.h>
#include <boost/filesystem/path.hpp>
#include <iostream>

struct SimulationResult
{
	bool failed; // did the top level event occur?
	bool valid;
	int failureTime; // number of logical time steps until the failure event
};


class Simulation
{
public:
	Simulation(
		const boost::filesystem::path& p, 
		int simulationTime, // the maximum duration of one simulation in seconds
		int simulationSteps, // the number of logical simulation steps performed in each round
		int numRounds) : // the number of simulation rounds for the entire net
		m_netFile(p),
		m_topProbability(0.0),
		m_failureTime(0),
		m_simulationTimeSeconds(simulationTime),
		m_numSimulationSteps(simulationSteps),
		m_numRounds(numRounds),
		m_bRunning(false){};

	virtual ~Simulation() { assert(!m_bRunning); };

	virtual bool run(bool withLogging = true) = 0;

protected:
	boost::filesystem::path m_netFile;
	
	bool m_bRunning;

	int m_simulationTimeSeconds;
	int m_numSimulationSteps;
	int m_numRounds;

	double m_topProbability;
	int m_failureTime; // the simulation step at which the top event was activated
};