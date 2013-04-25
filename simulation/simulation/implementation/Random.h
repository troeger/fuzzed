#pragma once
#include <random>
#include <map>
#include <fstream>
#include <boost/interprocess/managed_mapped_file.hpp>

using namespace std;
// using boost::interprocess;

class RandomNumberGenerator
{
public:
	// static RandomNumberGenerator& instance();
	virtual ~RandomNumberGenerator();
	RandomNumberGenerator();

	// uniform distribution
	double randomNumberInInterval(double L, double H);

	// exponential distribution
	double randomNumberExponential(double rate);

	int randomFiringTime(double rate);

	// weibull distribution
	double randomNumberWeibull(double rate, double k);

	double randomNumberDebug(double rate);

	int generateExponentialRandomNumbers(double rate, int count);

private:
#ifdef HIGH_PERFORMANCE
	linear_congruential_engine m_generator;
#else
	mt19937 m_generator;
#endif

	// create them lazily
	map<double, exponential_distribution<double>> m_exponentialDistributions;

	//ifstream m_randfile;
	
	int m_fileCount;
	string m_filePath;
};