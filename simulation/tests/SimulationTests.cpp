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
	EXPECT_SIMILAR(res.reliability, expectedReliability, MAX_DEVIATION);

namespace
{
	const string dir = "C:/dev/fuzztrees/simulation/testdata/faultTrees/";
	const string targetDir = "C:/dev/fuzztrees/simulation/tests/output/";

	const string AndOrTest			= "and_or.faulttree";
	const string ExampleSystemTest	= "example_system.faulttree";
	const string OrTest				= "single_or_gate.faulttree";
	const string AndTest			= "single_and_gate.faulttree";
	const string XorTest			= "single_xor_gate.faulttree";
	const string SEQTest			= "single_seq_gate.faulttree";
	const string BigTreeTest		= "big_tree.faulttree";
	const string SpareTest			= "single_spare_gate.faulttree";

	const int MISSION_TIME			= 1000;
	const int NUM_ROUNDS			= 10000;
	const double CONVERGE_THRESH	= 0.0;
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

	return res;
}

TEST(Simulation, AndOr)
{
	TEST_SIMULATION(dir + AndOrTest, 0.09);
}

TEST(Simulation, ExampleSystem)
{
	TEST_SIMULATION(dir + ExampleSystemTest, 0.5);
}

TEST(Simulation, And)
{
	TEST_SIMULATION(dir + AndTest, 0.6);
}

TEST(Simulation, Or)
{
	TEST_SIMULATION(dir + OrTest, 0.0);
}

TEST(Simulation, XOR)
{
	TEST_SIMULATION(dir + XorTest, 0.0);
}

TEST(Simulation, Sequence)
{
	TEST_SIMULATION(dir + SEQTest, 0.5);
}

TEST(Simulation, Convergence)
{ // run with a lower threshold and expect similar values but faster execution time
	string fn = dir + ExampleSystemTest;
	EXPECT_NO_THROW(runSimulation(_strdup(fn.c_str()), MISSION_TIME, NUM_ROUNDS, CONVERGE_THRESH * 100, MAX_TIME)); 
	util::replaceFileExtensionInPlace(fn, ".xml");
	SimulationResult res1 = readResultFile(fn);
	
	util::replaceFileExtensionInPlace(fn, ".faulttree");
	EXPECT_NO_THROW(runSimulation(_strdup(fn.c_str()), MISSION_TIME, NUM_ROUNDS, CONVERGE_THRESH, MAX_TIME)); 
	util::replaceFileExtensionInPlace(fn, ".xml");
	SimulationResult res2 = readResultFile(fn);

	EXPECT_SIMILAR(res1.reliability, res2.reliability, MAX_DEVIATION);
	EXPECT_LE(res1.duration, res2.duration, MAX_DEVIATION);
}

TEST(Simulation, BigTree)
{
	TEST_SIMULATION(dir + BigTreeTest, 0.5);
}

TEST(Simulation, Spare)
{
	TEST_SIMULATION(dir + SpareTest, 0.5);
}