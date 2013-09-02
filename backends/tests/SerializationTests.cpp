#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <gtest/gtest.h>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#if IS_WINDOWS 
	#pragma warning(pop) 
#endif

#include "serialization/PNMLDocument.h"
#include "serialization/TNDocument.h"
#include "FuzzTreeTransform.h"
#include "petrinet/PNMLImport.h"
#include "petrinet/PetriNet.h"
#include "util.h"
#include "Constants.h"

using namespace std;
using namespace boost;

#define TEST_NUM_CONFIGURATIONS(fileName, num)\
	auto ftTransform = FuzzTreeTransform(fileName);\
	EXPECT_EQ(ftTransform.transform().size(), num);

namespace
{
	const string dir = "C:/dev/fuzztrees/backends/simulation/testdata/configurations/";
	const string targetDir = "C:/dev/fuzztrees/backends/simulation/testdata/configurations/output/";

	const string optFileName			= "optional.fuzztree";
	const string optRedundancyFileName	= "optional_redundancy.fuzztree";
	const string otherName				= "other.fuzztree";
	const string redundancyFileName		= "redundancy.fuzztree";
	const string featureFileName		= "feature.fuzztree";
	const string exampleSystemFileName	= "example_system.fuzztree";
	const string config1				= "config1.fuzztree";
	const string intermediate			= "intermediate.fuzztree";
}

TEST(Serialization, PNML)
{
	static const string fileName = "test.pnml";	

	PNMLDocument doc;
	int tt = doc.addTimedTransition(0.001);
	
	int inPlace = doc.addPlace(1, 1, "Input");
	int outPlace = doc.addPlace(0, 1, "Output");

	doc.placeToTransition(inPlace, tt);
	doc.transitionToPlace(tt, outPlace);

	EXPECT_TRUE(doc.save(fileName));
	EXPECT_TRUE(doc.saved());
	EXPECT_TRUE(doc.valid());

	PetriNet* net = nullptr;
	EXPECT_NO_THROW(net = PNMLImport::loadPNML(fileName));
	EXPECT_NE(net, nullptr);

	EXPECT_EQ(net->numTimedTransitions() , 1);
	EXPECT_EQ(net->numPlaces(), 2);
	EXPECT_FALSE(net->hasInactiveTransitions());
}

TEST(Serialization, TN)
{
	static const string fileName = "test.TN";	

	TNDocument doc;
	int tt = doc.addTimedTransition(0.001);

	int inPlace = doc.addPlace(1, 1, "Input");
	int outPlace = doc.addPlace(0, 1, "Output");

	doc.placeToTransition(inPlace, tt);
	doc.transitionToPlace(tt, outPlace);

	EXPECT_TRUE(doc.save(fileName));
	EXPECT_TRUE(doc.saved());
	EXPECT_TRUE(doc.valid());
}

TEST(Serialization, Optional)
{
	TEST_NUM_CONFIGURATIONS(dir + optFileName, 2);
}

TEST(Serialization, FeatureVP)
{
	TEST_NUM_CONFIGURATIONS(dir + featureFileName, 6);
}

TEST(Serialization, Intermediate)
{
	TEST_NUM_CONFIGURATIONS(dir + intermediate, 1);
}

TEST(Serialization, RedundancyVP)
{
	TEST_NUM_CONFIGURATIONS(dir + redundancyFileName, 9); // 3*3 configs (two RedundancyVPs)
}

TEST(Serialization, Optional_Redundancy)
{
	TEST_NUM_CONFIGURATIONS(dir + optRedundancyFileName, 9); // 2*2 + 2 + 2 + 1 (no optional child)
}

TEST(Serialization, Other)
{
	TEST_NUM_CONFIGURATIONS(dir + otherName, 6);
}

TEST(Serialization, ExampleSystem)
{
	TEST_NUM_CONFIGURATIONS("C:/dev/fuzztrees/simulation/testdata/blocksim_compare/" + exampleSystemFileName, 3);
}

TEST(Serialization, Config1)
{
	TEST_NUM_CONFIGURATIONS(dir + config1, 5);
}