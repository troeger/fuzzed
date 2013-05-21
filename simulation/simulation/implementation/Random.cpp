#include "Random.h"
#include <time.h>
#include <iostream>
#include <omp.h>
#include <stdexcept>
#include "util.h"

RandomNumberGenerator::RandomNumberGenerator()
{
	static int count = 0;
	m_generator.seed(time(NULL) * ++count);
	// cout << "Creating Random Number Generator " << count << " in thread " << omp_get_thread_num() << endl;
}

double RandomNumberGenerator::randomNumberInInterval(double L, double H)
{
	uniform_real_distribution<double> dist(L, H);
	return dist(m_generator);
}

double RandomNumberGenerator::randomNumberExponential(double rate)
{
	auto res = m_exponentialDistributions.find(rate);
	if (res != m_exponentialDistributions.end())
		return res->second(m_generator);

	else
	{
		exponential_distribution<double> dist(rate);
		m_exponentialDistributions.insert(make_pair(rate, dist));
		return dist(m_generator);
	}
}

double RandomNumberGenerator::randomNumberWeibull(double rate, double k)
{
	weibull_distribution<double> dist(rate, k);
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
	return std::ceil(randomNumberExponential(rate));
}

boost::once_flag RandomNumberGenerator::s_flag  = BOOST_ONCE_INIT;
unordered_map<int, RandomNumberGenerator*> RandomNumberGenerator::s_generators = unordered_map<int, RandomNumberGenerator*>();

RandomNumberGenerator* RandomNumberGenerator::instanceForCurrentThread()
{
	if (s_generators.empty())
		boost::call_once(s_flag, initGenerators);
	
	assert(s_generators.size() > omp_get_thread_num());
	return s_generators.at(omp_get_thread_num());
}

void RandomNumberGenerator::initGenerators()
{
	for (int i = 0; i < omp_get_max_threads(); ++i)
		s_generators[i] = new RandomNumberGenerator();
}
