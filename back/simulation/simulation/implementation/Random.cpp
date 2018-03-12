#include "Random.h"
#include <time.h>
#include <iostream>
#include <stdexcept>
#include <cassert>
#include <limits.h>
#include "util.h"

#ifdef OMP_PARALLELIZATION
#include <omp.h>
#endif

using std::unordered_map;

RandomNumberGenerator::RandomNumberGenerator()
{
	// static int count = 0;
	m_generator.seed(time(NULL) * rand());
	// cout << "Creating Random Number Generator " << count << " in thread " << omp_get_thread_num() << endl;
}

double RandomNumberGenerator::randomNumberInInterval(double L, double H)
{
	uniform_real_distribution<double> dist(L, H);
	return dist(m_generator);
}

double RandomNumberGenerator::randomNumberExponential(double rate)
{
	if (rate <= 0.0)
		return std::numeric_limits<int>::max(); // this is undefined.

	exponential_distribution<double> dist(rate);
	return dist(m_generator);
}

void RandomNumberGenerator::generateExponentialRandomNumbers(const string& fileName, double rate, int count)
{
	ofstream file(fileName.c_str());
	if (!file.good()) throw std::runtime_error("Could not open file for random numbers");
	
	mt19937 gen;
	gen.seed(time(NULL));
	exponential_distribution<double> dist(rate);

	int i = 0;
	while (++i < count)
		file << util::toString(dist(gen)).c_str() << endl;

	file.close();
}

unsigned int RandomNumberGenerator::randomFiringTime(double rate)
{
	unsigned int t = std::ceil(randomNumberExponential(rate));
	return t;
}

RandomNumberGenerator::GeneratorMap RandomNumberGenerator::s_generators = RandomNumberGenerator::GeneratorMap();

RandomNumberGenerator* RandomNumberGenerator::instanceForCurrentThread()
{ 
#ifndef OMP_PARALLELIZATION
	const auto tid = std::this_thread::get_id();
	if (!CONTAINS(s_generators, tid))
	{
		s_generators[tid] = new RandomNumberGenerator();
	}
	return s_generators[tid];
#else
	return s_generators[omp_get_thread_num()];
#endif
}

void RandomNumberGenerator::initGenerators()
{
#ifdef OMP_PARALLELIZATION
	for (unsigned int i = 0; i < std::thread::hardware_concurrency(); ++i)
		s_generators[i] = new RandomNumberGenerator();
#endif
}

void RandomNumberGenerator::reseed()
{
#ifdef OMP_PARALLELIZATION
	static int k = 0;
	for (unsigned int i = 0; i < std::thread::hardware_concurrency(); ++i)
		s_generators[i]->m_generator.seed(++k);
#endif
}
