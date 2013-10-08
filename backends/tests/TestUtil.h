#pragma once
#include <string>

struct SimulationResult;
SimulationResult readResultFile(const std::string& fn);

#define EXPECT_SIMILAR(expected, actual, maxDeviation) EXPECT_TRUE(std::abs(expected - actual) <= maxDeviation)

#define TEST_SIMULATION(fileName, expectedReliability) \
	string fn = fileName; \
	EXPECT_NO_THROW(runSimulationOnFile(_strdup(fn.c_str()), NUM_ROUNDS, CONVERGE_THRESH, MAX_TIME)); \
	util::replaceFileExtensionInPlace(fn, ".xml"); \
	SimulationResult res = readResultFile(fn); \
	EXPECT_SIMILAR(res.reliability, expectedReliability, MAX_DEVIATION);