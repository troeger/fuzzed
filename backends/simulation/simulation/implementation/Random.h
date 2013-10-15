#pragma once
#include <random>
#include <unordered_map>
#include <fstream>
#include <mutex>

using namespace std;

class RandomNumberGenerator
{
public:
	static RandomNumberGenerator* instanceForCurrentThread();
	static void reseed();

	// uniform distribution
	double randomNumberInInterval(double L, double H);

	// exponential distribution
	double randomNumberExponential(double rate);
	unsigned int randomFiringTime(double rate);

	double randomNumberWeibull(double rate, double k);
	
	static void generateExponentialRandomNumbers(const string& fileName, double rate, int count);

	// this is a weird per-thread singleton pattern.
	static void initGenerators();

private:
	RandomNumberGenerator();

	mt19937 m_generator;
	unordered_map<double, exponential_distribution<double>> m_exponentialDistributions;

	static unordered_map<int, RandomNumberGenerator*> s_generators;
};