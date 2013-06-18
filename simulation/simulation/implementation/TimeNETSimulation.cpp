#include "TimeNETSimulation.h"

#include "util.h"

#include <fstream>
#include <iostream>
#include <sstream>
#include <cstdlib>

#include <boost/format.hpp>
#include <boost/filesystem.hpp>

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
#include <io.h>
#include <process.h>
#else
#include <stdio.h>
#endif

using boost::format;

#define JS_TEMPLATE_PATH "C:/dev/masterarbeit/simulation/repeat.js";

TimeNETSimulation::TimeNETSimulation(const boost::filesystem::path &p, 
									 int simulationTime, // the maximum duration of one simulation in seconds
									 int simulationSteps, // the number of logical simulation steps performed in each round
									 int numRounds,
									 void* args)
	: Simulation(p, simulationTime, simulationSteps, numRounds)
{
	TimeNETProperties* props = (TimeNETProperties*)(args);
	assert(props);

	m_properties = props;
	m_properties->filePath = p.generic_string();
}

bool TimeNETSimulation::run()
{
	string serverCall = 
		string("python ") + TNETSCRIPT 
		+ " " + m_properties->filePath
		+ " " + TNETDIR
		+ " " + util::toString(m_properties->transientSimTime)
		+ " " + util::toString(m_properties->confLevel)
		+ " " + util::toString(m_properties->epsilon)
		+ " " + util::toString(m_properties->seed)
		+ " " + util::toString(m_properties->maxExecutionTime);

	cout << "Simulation Parameters: " << endl << serverCall;

	int ret = system(serverCall.c_str());
	return (ret == 0);
}