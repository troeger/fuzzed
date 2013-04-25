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

	m_serverIP				= props->serverIP;
	m_resultIP				= props->resultIP;
	m_serverPort			= props->serverPort; 
	m_resultPort			= props->resultPort;
	m_integrationPropsPath	= props->integrationPropsPath; 
	m_logPropsPath			= props->logPropsPath;
	m_simulationServerPath	= props->simulationServerPath;
	m_filePath				= props->filePath;

	char* timenetDir = getenv("TIMENET_DIR");
	if (!timenetDir)
	{
		cout << "Could not find TIMENET_DIR. Please set this environment variable to the directory where TimeNET.jar resides." << endl;
		exit(EXIT_FAILURE);
	}
	m_timenetHome = boost::filesystem::path(timenetDir);
}

bool TimeNETSimulation::run(bool withLogging /*= true*/)
{
	const string jsPath = "./simulate.js";
	const string netFilePath = boost::filesystem::path(
		m_timenetHome.string() + "/" + m_filePath.filename().generic_string()).generic_string();

	util::copyFile(m_filePath.generic_string(), netFilePath);

	const char* templatePath = JS_TEMPLATE_PATH;
	ifstream inJS(templatePath, ios::in|ios::ate);
	if (!inJS.good())
		throw runtime_error("Could not load JavaScript template.");

	const int templateSize = (int)inJS.tellg();
	inJS.seekg(0, ios::beg);
	char* buf = (char*) malloc (templateSize*sizeof(char));
	memset(buf, 0, templateSize*sizeof(char));

	ofstream outJS(jsPath);
	if (!outJS.is_open())
		throw runtime_error("Could not open JavaScript file.");

	// javascript generation
	// parameters:
	// 	 count = %1%;
	// 	 simulationTime = %2%;
	// 	 netName = \"%3%\"
	// 	 sometimes: fileName = \"%4%\"

	inJS.read(buf, templateSize);
	const string outStr = str(format(buf) 
		% m_numRounds 
		% m_simulationTimeSeconds 
		% netFilePath);
	outJS << outStr.c_str();
	outJS.close();

	string serverCall = str(format("java -Xms32m -Xmx512m -cp %1% -DTNETHOME=\"%6%\" -Dlog4j.configuration=\"%2%\" gpsc.Host -i \"%3%\" -s -m \"%4%\" \"%5%\"") 
		% m_simulationServerPath 
		% m_logPropsPath % m_integrationPropsPath
		% m_timenetHome.generic_string() % jsPath
		% m_timenetHome);

	cout << "Simulation Parameters: " << endl << serverCall;
	
	char buffer[128];

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
	FILE* pipe = _popen(serverCall.c_str(), "rt");
#else
	FILE* pipe = popen(serverCall.c_str(), "rt");
#endif

	while (fgets(buffer, 128, pipe) != NULL)
	{
		string str = string(buffer);
		cout << str;
		if (str.find("###") != string::npos)
			return true;
	}

	// int ret = system(serverCall.c_str());
	// int ret = _execvp("java", serverCall.c_str());
	return false;
}