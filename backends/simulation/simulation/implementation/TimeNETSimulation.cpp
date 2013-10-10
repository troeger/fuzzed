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
	int ret;
#ifdef TNETDIR
#define RELIABILITY_DISTRIBUTION
#ifdef RELIABILITY_DISTRIBUTION
	auto fileName = m_properties->filePath;
	util::replaceFileExtensionInPlace(fileName, ".statistics_timenet");
	ofstream statdoc(fileName);
	statdoc << std::endl;

	const auto maxTime = m_properties->transientSimTime;
	for (int k = 1; k < maxTime; ++k)
	{
		m_properties->transientSimTime = k;
#endif
	const string serverCall = 
		string("python ") + TNETSCRIPT 
		+ " " + m_properties->filePath
		+ " " + TNETDIR
		+ " " + util::toString(m_properties->transientSimTime)
		+ " " + util::toString(m_properties->confLevel)
		+ " " + util::toString(m_properties->epsilon)
		+ " " + util::toString(m_properties->seed)
		+ " " + util::toString(m_properties->maxExecutionTime);

	cout << "Simulation Parameters: " << endl << serverCall;

	ret = system(serverCall.c_str());
	
	double r = -1.0;
	parseReliability(r);

#ifdef RELIABILITY_DISTRIBUTION
	statdoc << util::toString(1.0 - r) << std::endl;
	}
#endif
	return (ret == 0);
#endif // TNETDIR

	cout << "TimeNET not configured through CMake. Please check the USE_TIMENET option." << endl;
	return -1;
}

TimeNETSimulation::~TimeNETSimulation()
{
	if (m_properties)
		delete m_properties;
}

void TimeNETSimulation::parseReliability(double& res)
{
	auto fileName = m_properties->filePath;
	util::replaceFileExtensionInPlace(fileName, ".RESULTS");
	std::ifstream resultDoc(fileName);
	if (!resultDoc.good())
		return;

	std::string line;
	while (std::getline(resultDoc, line))
	{
		if (line.find("S") != 0) continue;
		// correct line
		const auto eqpos = line.find("=");
		const auto foo = line.substr(eqpos+1, line.length()-1);
		std::stringstream i;
		i << foo;
		double x = 0.0;
		if (i >> x)
			res = x;
	}
}

void TimeNETSimulation::tidyUp()
{
	// TODO
}
