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


TEST(Serialization, FuzzTreeTransform)
{
	static const string dir = "C:/dev/fuzztrees/simulation/testdata/configurations/";
	static const string targetDir = "C:/dev/fuzztrees/simulation/tests/output/";

	static const string optFileName			= "optional.fuzztree";
	static const string nestedFVPFileName	= "nestedFVP.fuzztree";
	static const string redundancyFileName	= "redundancy.fuzztree";
	static const string featureFileName		= "feature.fuzztree";
	
	ASSERT_TRUE(filesystem::create_directory(targetDir));

	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + optFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 2);

	filesystem::directory_iterator end;
	for(filesystem::directory_iterator iter(targetDir) ; iter != end ; ++iter)
		filesystem::remove_all(*iter);
	
	EXPECT_NO_THROW(FuzzTreeTransform::transformFuzzTree(dir + featureFileName, targetDir));
	EXPECT_EQ(util::countFiles(targetDir, faultTree::FAULT_TREE_EXT), 6);

	filesystem::remove_all(targetDir);
}