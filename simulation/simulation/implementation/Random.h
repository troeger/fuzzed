#pragma once
#include <random>
#include <boost/thread/once.hpp>
#include <unordered_map>
#include <fstream>

using namespace std;

class RandomNumberGenerator
{
public:
	static RandomNumberGenerator* instanceForCurrentThread();

	// uniform distribution
	double randomNumberInInterval(double L, double H);

	// exponential distribution
	double randomNumberExponential(double rate);
	unsigned int randomFiringTime(double rate);

	double randomNumberWeibull(double rate, double k);
	
	static void generateExponentialRandomNumbers(const string& fileName, double rate, int count);

private:
	RandomNumberGenerator();

	mt19937 m_generator;
	unordered_map<double, exponential_distribution<double>> m_exponentialDistributions;

	// this is a weird per-thread singleton pattern.
	static void initGenerators();
	static unordered_map<int, RandomNumberGenerator*> s_generators;
	static boost::once_flag s_flag;
};