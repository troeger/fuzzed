#include <gtest/gtest.h>

#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include "pugixml.hpp"
#if IS_WINDOWS 
#pragma warning(pop)
#endif

#include "SimulationProxy.h"
#include "ResultStruct.h"
#include "Constants.h"
#include "util.h"

#define EXPECT_SIMILAR(expected, actual, maxDeviation) EXPECT_TRUE(std::abs(expected - actual) <= maxDeviation)

#define TEST_SIMULATION(fileName, expectedReliability) \
	string fn = fileName; \
	EXPECT_NO_THROW(runSimulation(_strdup(fn.c_str()), MISSION_TIME, NUM_ROUNDS, CONVERGE_THRESH, MAX_TIME)); \
	util::replaceFileExtensionInPlace(fn, ".xml"); \
	SimulationResult res = readResultFile(fn); \
	EXPECT_SIMILAR(res.reliability, expectedReliability, MAX_DEVIATION); \
	EXPECT_GT(res.nRounds, 0); \
	EXPECT_GE(res.mttf, 0.0); \
	EXPECT_GE(res.meanAvailability, 0.0); \
	EXPECT_LE(res.duration, MAX_TIME);


namespace
{
	const string dir = "C:/dev/fuzztrees/simulation/testdata/faultTrees/";
	const string targetDir = "C:/dev/fuzztrees/simulation/tests/output/";

	const string AndOrTest			= "and_or.faulttree";
	const string ExampleSystemTest	= "example_system.faulttree";
	const string AndTest			= "single_and_gate.faulttree";
	const string OrTest				= "single_or_gate.faulttree";
	const string PANDTest			= "single_pand_gate.faulttree";
	const string SpareTest			= "single_spare_gate.faulttree";
	const string VotingOrTest		= "single_voting_or_gate.faulttree";

	const int MISSION_TIME			= 1000;
	const int NUM_ROUNDS			= 10000;
	const double CONVERGE_THRESH	= 0.00001;
	const int MAX_TIME				= 1000;
	const double MAX_DEVIATION		= 0.02; // TODO how much precision is needed here?
}

using namespace simulation;
using namespace pugi;

SimulationResult readResultFile(const string& fileName)
{
	SimulationResult res;
	xml_document resultDoc;
	if (!resultDoc.load_file(fileName.c_str()))
		return res;
	xml_node topNode = resultDoc.child(SIMULATION_RESULT);
	if (topNode.empty())
		return res;
	
	res.reliability			= topNode.attribute(RELIABILITY).as_double(-1.0);
	res.meanAvailability	= topNode.attribute(AVAILABILTIY).as_double(-1.0);
	res.mttf				= topNode.attribute(MTTF).as_double(-1.0);
	res.nRounds				= topNode.attribute(NROUNDS).as_uint(0);
	res.nFailures			= topNode.attribute(NFAILURES).as_uint(0);
	res.duration			= topNode.attribute(DURATION).as_uint(0);
	return res;
}

TEST(Simulation, AndOr)
{
	TEST_SIMULATION(dir + AndOrTest, 0.094);
}

TEST(Simulation, ExampleSystem)
{
	TEST_SIMULATION(dir + ExampleSystemTest, 0.58);
}

TEST(Simulation, Spare)
{
	TEST_SIMULATION(dir + SpareTest, 0.756);
}

TEST(Simulation, And)
{
	TEST_SIMULATION(dir + AndTest, 0.623);
}

TEST(Simulation, Or)
{
	TEST_SIMULATION(dir + OrTest, 0.02);
}

TEST(Simulation, VotingOR)
{
	TEST_SIMULATION(dir + VotingOrTest, 0.141);
}


// TODO: get some comparison values for PAND and SEQ