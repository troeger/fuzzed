#pragma once
#include "FaultTreeNode.h"

#include <assert.h>
#include <boost/filesystem/path.hpp>
#include <iostream>

struct SimulationRoundResult
{
	bool failed; // did the top level event occur?
	bool valid;
	unsigned int failureTime; // number of logical time steps until the failure event
};

class Simulation
{
public:
	Simulation(
		const boost::filesystem::path& p, 
		unsigned int simulationTime, // the maximum duration of one simulation in seconds
		unsigned int simulationSteps, // the number of logical simulation steps performed in each round
		unsigned int numRounds) : // the number of simulation rounds for the entire net
		m_netFile(p),
		m_simulationTimeSeconds(simulationTime),
		m_numSimulationSteps(simulationSteps),
		m_numRounds(numRounds),
		m_bRunning(false) {};


	Simulation(
		std::auto_ptr<FaultTreeNode> tree, 
		unsigned int simulationTime, // the maximum duration of one simulation in seconds
		unsigned int simulationSteps, // the number of logical simulation steps performed in each round
		unsigned int numRounds) : // the number of simulation rounds for the entire net
		m_netFile(""),
		m_faultTree(tree),
		m_simulationTimeSeconds(simulationTime),
		m_numSimulationSteps(simulationSteps),
		m_numRounds(numRounds),
		m_bRunning(false) {};

	virtual ~Simulation() { assert(!m_bRunning); };

	virtual bool run() = 0;

protected:
	boost::filesystem::path m_netFile;
	std::auto_ptr<FaultTreeNode> m_faultTree;
	
	bool m_bRunning;

	unsigned int m_simulationTimeSeconds;
	unsigned int m_numSimulationSteps;
	unsigned int m_numRounds;
};