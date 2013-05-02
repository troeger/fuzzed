#pragma once
#include "Simulation.h"

using namespace std;

struct TimeNETProperties
{
	string serverIP;
	int serverPort;
	string resultIP;
	int resultPort;
	
	string filePath; // the petri net file

	string integrationPropsPath;
	string logPropsPath;
	string simulationServerPath;
};

class TimeNETSimulation : public Simulation
{
public:
	TimeNETSimulation(
		const boost::filesystem::path& p, 
		int simulationTime, // the maximum duration of one simulation in seconds
		int simulationSteps, // the number of logical simulation steps performed in each round
		int numRounds,
		void* additionalArgmuments);
	virtual ~TimeNETSimulation() {}; // TODO

	virtual bool run() override;

protected:
	static const char* templatePath;

	int m_serverPort;
	int m_resultPort;

	std::string m_serverIP;
	std::string m_resultIP;

	boost::filesystem::path m_filePath;
	boost::filesystem::path m_simulationServerPath;
	boost::filesystem::path m_timenetHome;

	boost::filesystem::path m_integrationPropsPath;
	boost::filesystem::path m_logPropsPath;
};