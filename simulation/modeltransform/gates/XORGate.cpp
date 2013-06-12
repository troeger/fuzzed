#include "XORGate.h"
#include "serialization/TimeNETDocument.h"
#include <iostream>

using namespace std;

XORGate::XORGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

int XORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int oneChildFailed			= doc->addPlace(0, 1, "XOR_Failed");
	int failedChildren			= doc->addPlace(0, childIDs.size(), "Failed_Children");
	
	for (int id : childIDs)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		int propagateChildFailure = doc->addImmediateTransition();

		doc->placeToTransition(id, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, failedChildren, 1);
	}

	for (unsigned int i = 2; i <= childIDs.size(); ++i)
	{
		int discardMultipleFailures = doc->addImmediateTransition(2, "more than one child failed");
		doc->placeToTransition(failedChildren, discardMultipleFailures, i);
	}

	int finalTransition = doc->addImmediateTransition(1, "Trigger_XOR");
	doc->placeToTransition(failedChildren, finalTransition, 1);
	doc->transitionToPlace(finalTransition, oneChildFailed, 1);
	return oneChildFailed;
}

FaultTreeNode* XORGate::clone() const 
{
	FaultTreeNode* newNode = new XORGate(m_id, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}
