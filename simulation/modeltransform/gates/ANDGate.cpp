#include "ANDGate.h"
#include <vector>
#include "serialization/PNDocument.h"
#include "util.h"

using namespace std;

ANDGate::ANDGate(int id, const string& name /*= ""*/)
	: Gate(id, name)
{
	m_bDynamic = false;

	m_activationFunc = [](NodeValueMap childValues) -> long double 
	{
		long double result = 1.0;
		for (const auto& p : childValues)
			result *= p.second;

		return result;
	};
}

int ANDGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));
	
	int triggerGate = doc->addImmediateTransition();
	for (int id : childIDs)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		doc->placeToTransition(id, triggerGate);
	}
	
	int allChildrenFailed = doc->addPlace(0, 1, "AND_Failed");
	doc->transitionToPlace(triggerGate, allChildrenFailed);
	
	// cout << "Value of AND: " << getValue() << endl;

	return allChildrenFailed;
}

ANDGate::~ANDGate(void)
{}

FaultTreeNode* ANDGate::clone() const
{
	FaultTreeNode* newNode = new ANDGate(m_id, m_name);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}
