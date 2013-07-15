#include "SpareGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

#include <set>

SpareGate::SpareGate(const std::string& id, const set<string>& spareIndices, const double& dormancyFactor, const string& name)
	: DynamicGate(id, name), 
	m_spareIndices(spareIndices),
	m_dormancyFactor(dormancyFactor)
{}

int SpareGate::serializePTNet(boost::shared_ptr<PNDocument> doc) const 
{
	vector<pair<int,int>> spares;
	vector<int> regularIds;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
	{
		BasicEvent* basicEvent = dynamic_cast<BasicEvent*>(*it);
		if (CONTAINS(m_spareIndices, basicEvent->getId())) // TODO
			spares.push_back(basicEvent->serializeAsColdSpare(doc));
		else
			regularIds.push_back(basicEvent->serializePTNet(doc));
	}

	const int allFailed	= doc->addPlace(0, getNumChildren(), "SpareGateFailure");
	const int failGate	= doc->addImmediateTransition();
	
	// this place is shared between all primary gates and used to trigger spare activation
	const int primaryGateFailed	= doc->addPlace(0, regularIds.size(), "PrimaryGateFailure");
	
	for (const pair<int,int>& spare : spares)
	{
		doc->placeToTransition(primaryGateFailed, spare.second);
		doc->placeToTransition(spare.first, failGate);
	}

	for (const int& primary : regularIds)
	{
		// if a regular child fails, generate a token for spare activation
		int fail = doc->addImmediateTransition();
		doc->placeToTransition(primary, fail);
		doc->transitionToPlace(fail, primaryGateFailed);

		int failed = doc->addPlace(0, 1, "SingleSpareFailure");
		doc->transitionToPlace(fail, failed);
		doc->placeToTransition(failed, failGate);
	}

	doc->transitionToPlace(failGate, allFailed);
	return allFailed;
}

FaultTreeNode* SpareGate::clone() const
{
	FaultTreeNode* newNode = new SpareGate(m_id, m_spareIndices, m_dormancyFactor, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}
