#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <gtest/gtest.h>
#if IS_WINDOWS 
	#pragma warning(pop) 
#endif


#include "serialization/TimeNETDocument.h"
#include "serialization/PNMLDocument.h"
#include "FaultTreeIncludes.h"
#include "gates/RedundancyGate.h"

const string folder = "C:/dev/masterarbeit/tests/output/";

TEST(SingleGate, ANDGate)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ANDGate(1);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));

	EXPECT_EQ(ag->getNumChildren(), 2);
	EXPECT_EQ(faultTree.getNumChildren(), 1);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("AND Gate with 2 Basic Events with rate 0.0001");
	doc->save(folder+"test_and.pnml");
}


TEST(SingleGate, ORGate)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ORGate(1);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));
	
	EXPECT_EQ(ag->getNumChildren(), 2);
	EXPECT_EQ(faultTree.getNumChildren(), 1);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("OR Gate with 2 Basic Events with rate 0.0001");
	doc->save(folder+"test_or.pnml");
}

TEST(SingleGate, MultiAND)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ANDGate(1);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));
	ag->addChild(new BasicEvent(4, 0.0001));
	ag->addChild(new BasicEvent(5, 0.0001));
	ag->addChild(new BasicEvent(6, 0.0001));
	ag->addChild(new BasicEvent(7, 0.0001));

	EXPECT_EQ(ag->getNumChildren(), 6);
	EXPECT_EQ(faultTree.getNumChildren(), 1);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("AND Gate with 7 Basic Events with rate 0.0001");
	doc->save(folder+"test_and_multi.pnml");
}

TEST(MultipleGates, ANDOR)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ANDGate(1);
	faultTree.addChild(ag);

	FaultTreeNode* og1 = new ORGate(2);
	og1->addChild(new BasicEvent(3, 0.1));
	og1->addChild(new BasicEvent(4, 0.1));
	
	FaultTreeNode* og2 = new ORGate(5);
	og2->addChild(new BasicEvent(6, 0.1));
	og2->addChild(new BasicEvent(7, 0.1));

	ag->addChild(og1);
	ag->addChild(og2);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("AND Gate with two OR Gate children, each with two Basic Events with rate 0.1");
	doc->save(folder+"test_and_or.pnml");
}


TEST(MultipleGates, ANDOR2)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ANDGate(1);
	faultTree.addChild(ag);

	ag->addChild(new BasicEvent(2, 0.19));
	ag->addChild(new BasicEvent(3, 0.19));

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("Single AND Gate with two Basic Events with rate 0.19, equivalent to the AND-OR from above");
	doc->save(folder+"test_and_or_equiv.pnml");
}

TEST(StaticGates, VotingOR)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* vog = new VotingORGate(1, 2);
	faultTree.addChild(vog);

	vog->addChild(new BasicEvent(2, 0.01));
	vog->addChild(new BasicEvent(3, 0.01));
	vog->addChild(new BasicEvent(4, 0.01));
	vog->addChild(new BasicEvent(5, 0.01));

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("VotingOR with 2 out of 4 Basic Events with rate 0.01");
	doc->save(folder+"test_voting_or.pnml");
}

TEST(SingleGate, MultiOR)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ORGate(1);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));
	ag->addChild(new BasicEvent(4, 0.0001));
	ag->addChild(new BasicEvent(5, 0.0001));
	ag->addChild(new BasicEvent(6, 0.0001));
	ag->addChild(new BasicEvent(7, 0.0001));

	EXPECT_EQ(ag->getNumChildren(), 6);
	EXPECT_EQ(faultTree.getNumChildren(), 1);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("OR Gate with 7 Basic Events with rate 0.0001");
	doc->save(folder+"test_or_multi.pnml");
}


TEST(SingleGate, MultiORProbable)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new ORGate(1);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.1));
	ag->addChild(new BasicEvent(3, 0.1));
	ag->addChild(new BasicEvent(4, 0.1));
	ag->addChild(new BasicEvent(5, 0.1));
	ag->addChild(new BasicEvent(6, 0.1));
	ag->addChild(new BasicEvent(7, 0.1));

	EXPECT_EQ(ag->getNumChildren(), 6);
	EXPECT_EQ(faultTree.getNumChildren(), 1);

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("OR Gate with 7 Basic Events with rate 0.1");
	doc->save(folder+"test_or_probable.pnml");
}

TEST(SingleGate, VotingORGate)
{
	TopLevelEvent faultTree(0);
	FaultTreeNode* ag = new VotingORGate(1, 3);
	faultTree.addChild(ag);

	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));
	ag->addChild(new BasicEvent(4, 0.0001));
	ag->addChild(new BasicEvent(5, 0.0001));

	boost::shared_ptr<TimeNETDocument> doc(new TimeNETDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("VotinOR Gate with 3 out of 4 Basic Events with rate 0.0001");
	doc->save(folder+"test_voting_or2.xml");
}

TEST(SingleGate, SpareGate)
{
	TopLevelEvent faultTree(0);

	set<int> spareIds;
	spareIds.insert(3);

	FaultTreeNode* ag = new SpareGate(1, spareIds, "SpareGate");
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));
	
	boost::shared_ptr<TimeNETDocument> doc(new TimeNETDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("Cold Spare Gate with 2 Basic Events with rate 0.0001");
	doc->save(folder+"test_spare.xml");
}

TEST(SingleGate, PANDGate)
{
	TopLevelEvent faultTree(0);
	std::set<int> prioIds;
	prioIds.insert(3);
	FaultTreeNode* ag = new PANDGate(1, prioIds);
	faultTree.addChild(ag);
	ag->addChild(new BasicEvent(2, 0.0001));
	ag->addChild(new BasicEvent(3, 0.0001));

	boost::shared_ptr<TimeNETDocument> doc(new TimeNETDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("PAND Gate with 2 Basic Events with rate 0.0001");
	doc->save(folder+"test_pand.xml");
}

TEST(SingleGate, IO)
{
	TimeNETDocument doc;
	int pid = doc.addPlace(3, 3);
	int tid = doc.addImmediateTransition();
	doc.placeToTransition(pid, tid);
	doc.transitionToPlace(tid, pid);

	EXPECT_FALSE(doc.empty());

	doc.save("petri.xml");
	EXPECT_TRUE(doc.saved());

	TimeNETDocument doc2 = TimeNETDocument("petri.xml");
	EXPECT_TRUE(doc2.valid());
}

TEST(SingleGate, BasicTest)
{
	TimeNETDocument doc;
	int pid = doc.addPlace(3, 3);
	int tid = doc.addImmediateTransition();
	doc.placeToTransition(pid, tid);

	EXPECT_FALSE(doc.empty());
}

TEST(Hierarchy, BasicTest)
{
	TopLevelEvent faultTree(0);
	std::set<int> s;
	s.insert(1);
	FaultTreeNode* ag = new PANDGate(1, s);
	faultTree.addChild(ag);

	FaultTreeNode* og = new ORGate(1);
	og->addChild(new BasicEvent(2, 0.0001));
	og->addChild(new BasicEvent(3, 0.0001));

	ag->addChild(og);
	ag->addChild(new BasicEvent(4, 0.0001));

	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	faultTree.serialize(doc);

	doc->addUserDescription("PAND Gate with one OR Gate with 2 Basic Events and one Basic Event, each with rate 0.0001");
	doc->save(folder+"test_pand_or.pnml");
}


TEST(Redundancy, FormulaTest)
{
	RedundancyGate rg(0, 2, 4, 3, "N-1", "RedundancyGate");
	EXPECT_EQ(rg.getNumVotes(),2);

	rg = RedundancyGate(0, 1, 5, 5, "N*2", "");
	EXPECT_EQ(rg.getNumVotes(), 10);
}