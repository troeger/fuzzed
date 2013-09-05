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

FaultTreeNode::Ptr SpareGate::clone() const
{
	FaultTreeNode::Ptr newNode = make_shared<SpareGate>(m_id, m_primaryId, m_dormancyFactor, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}

int SpareGate::serializeTimeNet(std::shared_ptr<TNDocument> doc) const 
{
	// see FuzzTrees / simulation / modeltransform / timeNetModels / spare.xml
	const int spareGateFailed = doc->addPlace(0, 1);
	const int failSpareGate = doc->addImmediateTransition();

	// fail just once
	doc->transitionToPlace(failSpareGate, spareGateFailed);
	doc->addInhibitorArc(spareGateFailed, failSpareGate);
	
// 	static const string dormancy = "dormancyFactor";
// 	doc->addDefinition(dormancy, m_dormancyFactor); // not necessary actually

	const auto& primaryChild = getChildById(m_primaryId);
	const int primaryFailed = primaryChild->serializeTimeNet(doc);

	doc->placeToTransition(primaryFailed, failSpareGate);
	doc->transitionToPlace(failSpareGate, primaryFailed);

	// spares
	for (const auto& child : m_children)
	{
		if (child->getId() == m_primaryId) continue;

		// TODO: in theory, BasicEventSets and house/undeveloped events are allowed as well
		// the assumption is that BasicEventSets have previously been expanded
		auto be = dynamic_pointer_cast<BasicEvent>(child);
		if (!be) throw runtime_error("Spares must be BasicEvents");

		const auto failureRate = be->getFailureRate();
		const auto spare = be->serializeAsSpare(doc);

		const int spareRunning		= get<0>(spare);
		const int spareFailed		= get<1>(spare);
		const int failSparePassive	= get<2>(spare);

		const int spareActivated = doc->addPlace(0);
		const int activateSpare = doc->addImmediateTransition();
		doc->placeToTransition(spareRunning, activateSpare);
		doc->placeToTransition(primaryFailed, activateSpare);
		doc->transitionToPlace(activateSpare, spareActivated);

		// once the spare has become activated, it has a different failure distribution
		const int failSpareActive = doc->addTimedTransition(failureRate * m_dormancyFactor);
		doc->placeToTransition(spareActivated, failSpareActive);
		doc->addInhibitorArc(spareActivated, failSparePassive);
		doc->transitionToPlace(failSpareActive, spareFailed);

		doc->placeToTransition(spareFailed, failSpareGate);
		doc->transitionToPlace(failSpareGate, spareFailed);
	}

	return spareGateFailed;
}
