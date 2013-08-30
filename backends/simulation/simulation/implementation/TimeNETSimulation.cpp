#include "TimeNETSimulation.h"
#include "FaultTreeNode.h"
#include "serialization/TNDocument.h"

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

TimeNETSimulation::TimeNETSimulation(const boost::filesystem::path &p, 
									 int simulationTime, // the maximum duration of one simulation in seconds
									 int simulationSteps, // the number of logical simulation steps performed in each round
									 int numRounds,
									 void* args)
	: Simulation(p, simulationTime, simulationSteps, numRounds), m_properties(nullptr)
{
	TimeNETProperties* props = (TimeNETProperties*)(args);
	assert(props);

	m_properties = props;
	m_properties->filePath = p.generic_string();
}

TimeNETSimulation::TimeNETSimulation(std::shared_ptr<FaultTreeNode> faultTree, 
									 int simulationTime, /* the maximum duration of one simulation in seconds */ 
									 int simulationSteps, /* the number of logical simulation steps performed in each round */ 
									 int numRounds, 
									 void* additionalArgmuments)
	: Simulation(faultTree, simulationTime, simulationSteps, numRounds), m_properties(nullptr)
{
	TimeNETProperties* props = (TimeNETProperties*)(additionalArgmuments);
	assert(props);

	m_properties = props;
	const string TNpath = "foo.TN";

	std::shared_ptr<TNDocument> doc(new TNDocument);
	faultTree->serializePTNet(doc);
	doc->save(TNpath);
	m_properties->filePath = TNpath;
}

bool TimeNETSimulation::run()
{
#ifdef TNETDIR
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
#endif

	cout << "TimeNET not configured through CMake. Please check the USE_TIMENET option." << endl;
	return -1;
}

TimeNETSimulation::~TimeNETSimulation()
{
	if (m_properties)
		delete m_properties;
}
