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
#include "FuzzTreeTransform.h"
#include "petrinet/PNMLImport.h"
#include "petrinet/PetriNet.h"
#include "FaultTreeImport.h"
#include "util.h"
#include "Constants.h"

using namespace std;
using namespace boost;


namespace
{
	const string dir = "C:/dev/fuzztrees/simulation/testdata/configurations/";
	const string targetDir = "C:/dev/fuzztrees/simulation/tests/output/";

	const string optFileName			= "optional.fuzztree";
	const string nestedFVPFileName	= "nestedFVP.fuzztree";
	const string redundancyFileName	= "redundancy.fuzztree";
	const string featureFileName		= "feature.fuzztree";
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


TEST(Serialization, Optional)
{
	if (filesystem::is_directory(targetDir)) 
		filesystem::remove_all(targetDir);
	ASSERT_TRUE(filesystem::create_directory(targetDir));

	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + optFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 2);

}

TEST(Serialization, FeatureVP)
{
	if (filesystem::is_directory(targetDir)) 
		filesystem::remove_all(targetDir);
	ASSERT_TRUE(filesystem::create_directory(targetDir));
	
	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + featureFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 6);

	filesystem::remove_all(targetDir);
}

TEST(Serialization, RedundancyVP)
{
	if (filesystem::is_directory(targetDir)) 
		filesystem::remove_all(targetDir);
	ASSERT_TRUE(filesystem::create_directory(targetDir));
	
	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + redundancyFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 9); // 3*3 configs (two RedundancyVPs)

	filesystem::remove_all(targetDir);
}

TEST(Serialization, Other)
{
	if (filesystem::is_directory(targetDir)) 
		filesystem::remove_all(targetDir);
	ASSERT_TRUE(filesystem::create_directory(targetDir));
	
	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + nestedFVPFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 8);

	filesystem::remove_all(targetDir);
}