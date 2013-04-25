#include "VotingORGate.h"
#include "serialization/PNDocument.h"
#include "FaultTreeNode.h"
#include "util.h"

VotingORGate::VotingORGate(int id, int numVotes, const string& name) 
	: Gate(id, name), m_numVotes(numVotes)
{
	m_bDynamic = false;

	m_activationFunc = [=](NodeValueMap childValues) -> long double 
	{
		assert(childValues.size() > 0);

		// What to do if the children have different values?
		const long double rate = childValues.begin()->second;
		return util::kOutOfN(rate, numVotes, childValues.size());
	};
}


int VotingORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	if (getNumChildren() == 0)
		return -1;

	cout << "Value of VotingOR: " << getValue() << endl;

	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int somethingFailed = doc->addPlace(0, childIDs.size(), "VotingOR_somethingFailed");
	for (int id : childIDs)
	{
		int transitionID = doc->addImmediateTransition();
		doc->placeToTransition(id, transitionID, 1, "i");
		doc->transitionToPlace(transitionID, somethingFailed, 1, "i");
	}

	int finalTransitionID = doc->addImmediateTransition(2.0);
	doc->placeToTransition(somethingFailed, finalTransitionID, m_numVotes, "x");

	int gateFailed = doc->addPlace(0, 1, "VotingOR");
	doc->transitionToPlace(finalTransitionID, gateFailed);

	return gateFailed;
}

FaultTreeNode* VotingORGate::clone() const
{
	FaultTreeNode* newNode = new VotingORGate(m_id, m_numVotes, m_name);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}

std::string VotingORGate::description() const 
{
	return util::toString(m_numVotes) + " out of " + util::toString(getNumChildren());
}
