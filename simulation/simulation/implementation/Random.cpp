#include "Random.h"
#include <time.h>
#include <boost/lexical_cast.hpp>
#include <iostream>
#include "util.h"
#include "Config.h"

RandomNumberGenerator::RandomNumberGenerator()
	: m_fileCount(0)
{
	static int count = 0;
	m_generator.seed(++count);
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
	{
		const double rand =  res->second(m_generator);
		return rand;
	}
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

int RandomNumberGenerator::generateExponentialRandomNumbers(double rate, int count)
{
	const string fileName = m_filePath + "rand" + util::toString(++m_fileCount) + ".txt";
	ofstream file(fileName.c_str());
	if (!file.good())
		throw std::runtime_error("Could not open file for random numbers");
	
	exponential_distribution<double> dist(rate);

	int i = 0;
	while (++i < count)
	{
		file << util::toString(dist(m_generator)).c_str() << endl;
	}
	file.close();

	return m_fileCount;
}


// just a fast way of getting one random number with rate 0.001.
double RandomNumberGenerator::randomNumberDebug(double rate)
{
	exponential_distribution<double> dist(rate);
	return dist(m_generator);
}

RandomNumberGenerator::~RandomNumberGenerator()
{}

int RandomNumberGenerator::randomFiringTime(double rate)
{
	return std::ceil(randomNumberExponential(rate));
}
