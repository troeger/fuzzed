#include "XORGate.h"
#include "serialization/TimeNETDocument.h"

XORGate::XORGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

int XORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int oneChildFailed			= doc->addPlace(0, 1, "XOR_Failed");
	int moreThanOneChildFailed	= doc->addPlace(0, 0, "XOR_moreThanOne");
	for (int id : childIDs)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		int propagateChildFailure = doc->addImmediateTransition();

		doc->placeToTransition(id, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, oneChildFailed);
	}

	// doc->placeToTransition(oneChildFailed, discardMultipleFailures, 2); 
	// TODO: this should be ">=2". Or add transitions for every i < numChildren.
	for (int i = 2; i <= childIDs.size(); ++i)
	{
		int discardMultipleFailures = doc->addImmediateTransition(2.0, Condition(), "more than one child failed");
		doc->placeToTransition(oneChildFailed, discardMultipleFailures, i);
		doc->transitionToPlace(discardMultipleFailures, moreThanOneChildFailed, 0);
	}

	return oneChildFailed;
}

FaultTreeNode* XORGate::clone() const 
{
	FaultTreeNode* newNode = new XORGate(m_id, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}
