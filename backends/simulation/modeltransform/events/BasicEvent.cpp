#include "BasicEvent.h"
#include "gates/FDEPGate.h"
#include "serialization/PNDocument.h"
#include "util.h"

#include <stdexcept>
using std::runtime_error;

BasicEvent::BasicEvent(const std::string& ID, double failureRate, const std::string& name/* = ""*/, int cost /*=1*/)
	: Event(ID, failureRate, name),
	m_serializedPlaceID(-1)
{
	m_cost = cost;
}

int BasicEvent::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	if (m_serializedPlaceID != -1)
	{
		return m_serializedPlaceID;
	}
	
	int notFailed = doc->addPlace(1, 1, "BasicEvent" + m_id);
	int failComponent = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(notFailed, failComponent);
	
	int failed = doc->addPlace(0, 1, "BasicEvent" + m_id + "_occured");
	doc->transitionToPlace(failComponent, failed);

	serializeFDEPChildren(doc, failed);

	assert(failed >= 0);
	m_serializedPlaceID = failed;
	return failed;
}

FaultTreeNode::Ptr BasicEvent::clone() const
{
	return make_shared<BasicEvent>(m_id, m_failureRate, m_name, m_cost);
}

std::string BasicEvent::description() const 
{
	return FaultTreeNode::description() 
		+ " Rate: " + util::toString(m_failureRate);
}

std::pair<int /*placeID*/,int /*spareActivationTransition*/>
	BasicEvent::serializeAsColdSpare(std::shared_ptr<PNDocument> doc) const
{
	int sparePassive = doc->addPlace(1, 1, "ColdSpare" + m_id);
	int activateTransition = doc->addImmediateTransition();
	doc->placeToTransition(sparePassive, activateTransition);

	int activePlaceID = doc->addPlace(0, 1, "ColdSpare" + m_id + "_active");
	int failedPlaceID = doc->addPlace(0, 1, "ColdSpare" + m_id + "_failed");
	int failTransition = doc->addTimedTransition(m_failureRate);
	doc->transitionToPlace(activateTransition, activePlaceID);
	doc->placeToTransition(activePlaceID, failTransition);
	doc->transitionToPlace(failTransition, failedPlaceID);

	serializeFDEPChildren(doc, failedPlaceID);
	return make_pair(failedPlaceID, activateTransition);
}

std::tuple<int /*not failed*/, int /*failed*/, int /*failure transition*/> 
	BasicEvent::serializeAsSpare(std::shared_ptr<PNDocument> doc) const
{
	int notFailed = doc->addPlace(1, 1, "BasicEvent" + m_id);
	int failComponent = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(notFailed, failComponent);

	int failed = doc->addPlace(0, 1, "BasicEvent" + m_id + "_occured");
	doc->transitionToPlace(failComponent, failed);

	serializeFDEPChildren(doc, failed);

	return make_tuple(notFailed, failed, failComponent);
}

void BasicEvent::serializeFDEPChildren(std::shared_ptr<PNDocument> doc, const int& failedPlaceId) const
{
	if (getNumChildren() == 0) return;
	
	// each BasicEvent can be triggered by N FDEPs
	const int fdepTriggerTransition = doc->addImmediateTransition();
	for (const auto& child : m_children)
	{
		auto fdep = std::dynamic_pointer_cast<FDEPGate>(child);
		if (!fdep)
			throw runtime_error("Spares must be BasicEvents");
		// TODO differentiate between the different serialization implementations here?
		const int fdepTriggered = fdep->serializePTNet(doc);
		doc->placeToTransition(fdepTriggered, fdepTriggerTransition);
	}

	doc->transitionToPlace(fdepTriggerTransition, failedPlaceId);
	doc->addInhibitorArc(failedPlaceId, fdepTriggerTransition);
}

