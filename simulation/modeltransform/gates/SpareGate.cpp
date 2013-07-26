#include "SpareGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

#include <set>

SpareGate::SpareGate(const std::string& id, const std::string& primaryId, const double& dormancyFactor, const string& name)
	: DynamicGate(id, name), 
	m_primaryId(primaryId),
	m_dormancyFactor(dormancyFactor)
{}

int SpareGate::serializePTNet(boost::shared_ptr<PNDocument> doc) const 
{
	// just cold spare behaviour in PNML, regardless of dormancy factor
	// works only with basic events so far...
	
	vector<pair<int,int>> spares;
	vector<int> regularIds;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
	{
		BasicEvent* basicEvent = dynamic_cast<BasicEvent*>(*it);
		if (m_primaryId == basicEvent->getId()) // TODO
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
	FaultTreeNode* newNode = new SpareGate(m_id, m_primaryId, m_dormancyFactor, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}

int SpareGate::serializeTimeNet(boost::shared_ptr<TNDocument> doc) const 
{
	// see FuzzTrees / simulation / modeltransform / timeNetModels / spare.xml
	const int spareGateFailed = doc->addPlace(0);
	const int failSpareGate = doc->addImmediateTransition();

	// fail just once
	doc->transitionToPlace(failSpareGate, spareGateFailed);
	doc->addInhibitorArc(spareGateFailed, failSpareGate);
	
	static const string dormancy = "dormancyFactor";
	doc->addDefinition(dormancy, m_dormancyFactor);

	doc->addParametrisedTransition(dormancy + " * 2.0");

	return spareGateFailed;
}
