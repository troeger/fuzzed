#include "UndevelopedEvent.h"
#include <cassert>
#include "serialization/PNDocument.h"
#include "util.h"

int UndevelopedEvent::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	int placeID = doc->addPlace(1, 1, "UndevelopedEvent" + m_id);
	int transitionID = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(placeID, transitionID);
	placeID = doc->addPlace(0, 1);
	doc->transitionToPlace(transitionID, placeID);

	return placeID;
}

UndevelopedEvent::UndevelopedEvent(const std::string& ID, double failureRate, const string& name /*= ""*/) 
	: Event(ID, failureRate, name)
{}

void UndevelopedEvent::addChild(FaultTreeNode::Ptr)
{
	assert(false && "This is a leaf node!");
}

FaultTreeNode::Ptr UndevelopedEvent::clone() const
{
	return make_shared<UndevelopedEvent>(m_id, m_failureRate, m_name);
}
