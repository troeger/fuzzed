#include "VotingORGate.h"
#include "serialization/PNDocument.h"
#include "util.h"

VotingORGate::VotingORGate(const std::string& id, int numVotes, const string& name) 
	: StaticGate(id, name), m_numVotes(numVotes)
{
	initActivationFunc();
}

int VotingORGate::serializePTNet(boost::shared_ptr<PNDocument> doc) const 
{
	if (getNumChildren() == 0)
		return -1;

	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serializePTNet(doc));

	int somethingFailed = doc->addPlace(0, childIDs.size(), "VotingOR_somethingFailed");
	for (int childFailed : childIDs)
	{
		int propagateChildFailure = doc->addImmediateTransition();
		doc->placeToTransition(childFailed, propagateChildFailure, 1, "i");
		doc->transitionToPlace(propagateChildFailure, somethingFailed, 1, "i");
	}

	int triggerGate = doc->addImmediateTransition();
	doc->placeToTransition(somethingFailed, triggerGate, m_numVotes, "x");

	int gateFailed = doc->addPlace(0, 1, "VotingOR");
	doc->transitionToPlace(triggerGate, gateFailed);

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

std::string VotingORGate::serializeAsFormula(boost::shared_ptr<PNDocument> doc) const 
{
	vector<std::string> childFormulas;
	for (const auto child : m_children)
		childFormulas.emplace_back(child->serializeAsFormula(doc));

	const int numChildren = childFormulas.size();
	string res = s_formulaBegin;

	// we need all n-combinations with n in [numVotes, numChildren]
	for (int i = m_numVotes; i <= numChildren; ++i)
	{
		do
		{
			res += s_formulaBegin;
			res += childFormulas[0];
			for (int j = 1; j < i; ++j)
			{
				res += s_ANDoperator;
				res += childFormulas[j];
			}
			res += s_formulaEnd;
			res += s_ORoperator;

		} while (util::next_combination(childFormulas.begin(), childFormulas.begin() + i, childFormulas.end()));
	}
	res.erase(res.length() - s_ORoperator.length(), s_ORoperator.length()); // TODO remove last OR
	return res + s_formulaEnd;
}

void VotingORGate::initActivationFunc()
{
	m_activationFunc = [=](NodeValueMap childValues) -> long double 
	{
		assert(childValues.size() > 0);

		// What to do if the children have different values?
		const long double rate = childValues.begin()->second;
		return util::kOutOfN(rate, m_numVotes, childValues.size());
	};
}


