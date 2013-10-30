#pragma once
#include <random>
#include <unordered_map>
#include <fstream>
#include <mutex>
#include <thread>

#include "Config.h"

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
	
	static void generateExponentialRandomNumbers(const std::string& fileName, double rate, int count);

	// this is a weird per-thread singleton pattern.
	static void initGenerators();

private:
	RandomNumberGenerator();

	std::mt19937 m_generator;
	std::unordered_map<double, std::exponential_distribution<double>> m_exponentialDistributions;

#ifndef OMP_PARALLELIZATION
	typedef std::unordered_map<std::thread::id, RandomNumberGenerator*> GeneratorMap;
#else
	typedef std::unordered_map<int, RandomNumberGenerator*> GeneratorMap;
#endif


	static GeneratorMap s_generators;
};