#include <gtest/gtest.h>

#include "SimulationExtern.h"
#include "ResultStruct.h"
#include "Constants.h"
#include "util.h"

#define EXPECT_SIMILAR(expected, actual, maxDeviation) EXPECT_TRUE(std::abs(expected - actual) <= maxDeviation)

#define TEST_SIMULATION(fileName, expectedReliability) \
	string fn = fileName; \
	EXPECT_NO_THROW(runSimulationOnFile(_strdup(fn.c_str()), NUM_ROUNDS, CONVERGE_THRESH, MAX_TIME)); \
	util::replaceFileExtensionInPlace(fn, ".xml"); \
	SimulationResult res = util::readResultFile(fn); \
	EXPECT_SIMILAR(res.reliability, expectedReliability, MAX_DEVIATION);


namespace
{
	const string dir = "C:/dev/fuzztrees/simulation/testdata/faultTrees/";
	const string targetDir = "C:/dev/fuzztrees/simulation/tests/output/";

	const string ProbableOrTest		= "single_or_gate_probable.faulttree";
	const string ProbableXORTest	= "single_xor_gate_probable.faulttree";
	const string ProbablePandTest	= "single_pand_gate_probable.faulttree";

	const int MISSION_TIME			= 1000;
	const int NUM_ROUNDS			= 100000;
	const double CONVERGE_THRESH	= 0.00001;
	const int MAX_TIME				= 1000;
	const double MAX_DEVIATION		= 0.02; // TODO how much precision is needed here?
}

using namespace simulation;
using namespace pugi;

TEST(SingleStep, OR)
{
	TEST_SIMULATION(dir + ProbableOrTest, 0.25);
}

TEST(SingleStep, XOR)
{
	TEST_SIMULATION(dir + ProbableXORTest, 0.5);
}

TEST(SingleStep, Pand)
{
	TEST_SIMULATION(dir + ProbablePandTest, 0.875);
}
