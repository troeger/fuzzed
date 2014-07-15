#include "SpareGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

#include <set>
#include <stdexcept>

SpareGate::SpareGate(const std::string& id, const std::string& primaryId, const double& dormancyFactor, const string& name)
	: DynamicGate(id, name), 
	m_primaryId(primaryId),
	m_dormancyFactor(dormancyFactor)
{}

int SpareGate::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	// just cold spare behaviour in PNML, regardless of dormancy factor
	// works only with basic events so far...
	
	vector<pair<int,int>> spares;
	vector<int> regularIds;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
	{
		auto basicEvent = dynamic_pointer_cast<BasicEvent>(*it);
		assert(basicEvent);
		if (m_primaryId != basicEvent->getId()) // spare
			spares.push_back(basicEvent->serializeAsColdSpare(doc));
		else // primary
			regularIds.push_back(basicEvent->serializePTNet(doc));
	}

	if (spares.empty() || regularIds.empty())
		throw std::runtime_error("Spare gates need at least a spare and a primary component!");

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

FaultTreeNode::Ptr SpareGate::clone() const
{
	FaultTreeNode::Ptr newNode = make_shared<SpareGate>(m_id, m_primaryId, m_dormancyFactor, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}
