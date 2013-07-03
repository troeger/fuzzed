#include "ORGate.h"
#include "serialization/PNDocument.h"
#include <iostream>

using namespace std;

ORGate::ORGate(const string& id, const string& name /*= ""*/) 
	: StaticGate(id, name)
{
	initActivationFunc();
}

ORGate::~ORGate(void)
{
}

int ORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int oneChildFailed = doc->addPlace(0, 1, "OR_Failed");
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

	// cout << "Value of OR: " << computeUnreliability() << endl;

	return oneChildFailed;
}

FaultTreeNode* ORGate::clone() const
{
	FaultTreeNode* newNode = new ORGate(m_id, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());
	
	return newNode;
}

std::string ORGate::serializeAsFormula(boost::shared_ptr<PNDocument> doc) const 
{
	assert(false && "implement");
	return "";
}

void ORGate::initActivationFunc()
{
	m_activationFunc = [](NodeValueMap childValues) -> long double 
	{
		long double result = 1.0;
		for (const auto& p : childValues)
			result *= 1.0 - p.second;

		return 1.0L - result;
	};
}
