#include "XORGate.h"
#include "serialization/PNDocument.h"
#include "util.h"
#include <iostream>

using namespace std;

XORGate::XORGate(const std::string& ID, const std::string& name)
	: StaticGate(ID, name)
{}

int XORGate::serializePTNet(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serializePTNet(doc));

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

std::string XORGate::serializeAsFormula(boost::shared_ptr<PNDocument> doc) const
{
	vector<std::string> childFormulas;
	for (const auto child : m_children)
		childFormulas.emplace_back(child->serializeAsFormula(doc));

	const int numChildren = childFormulas.size();
	if (numChildren == 0) return "false";

	string res = s_formulaBegin;
	
	// first: the OR part
	res += s_formulaBegin + childFormulas[0];
	for (int i = 1; i < numChildren; ++i)
		res += s_ORoperator + childFormulas[i];
	res += s_formulaEnd;

	res += s_ANDoperator;

	// second: disallow any 2-combination
	do
	{
		res +=
			s_NOToperator + s_formulaBegin +
			childFormulas[0] + s_ANDoperator + childFormulas[1] +
			s_formulaEnd;
		
		res += s_ANDoperator;

	} while (util::next_combination(childFormulas.begin(), childFormulas.begin() + 2, childFormulas.end()));
	res.erase(res.length() - s_ANDoperator.length(), s_ANDoperator.length()); // TODO remove last AND

	return res + s_formulaEnd;
}

void XORGate::initActivationFunc()
{
	// ???
}
