#include "BasicEvent.h"
#include "serialization/PNDocument.h"
#include "util.h"

BasicEvent::BasicEvent(int ID, long double failureRate, const std::string& name/* = ""*/, int cost /*=1*/)
	: Event(ID, failureRate, name)
{
	m_cost = cost;
}

BasicEvent::~BasicEvent()
{}

int BasicEvent::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	int placeID = doc->addPlace(1, 1, "BasicEvent" + util::toString(m_id), true);
	int transitionID = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(placeID, transitionID);
	placeID = doc->addPlace(0, 100, "BasicEvent" + util::toString(m_id) + "_occured");
	doc->transitionToPlace(transitionID, placeID);

	return placeID;
}

void BasicEvent::addChild(FaultTreeNode* child)
{
	assert(false && "This is a leaf node!");
}

std::pair<int,int> BasicEvent::serializeAsColdSpare(boost::shared_ptr<PNDocument> doc) const
{
	int spare = doc->addPlace(1, 1, "ColdSpare" + util::toString(m_id), true);
	int activateTransition = doc->addImmediateTransition();
	doc->placeToTransition(spare, activateTransition);
	
	int activePlaceID = doc->addPlace(0, 1, "ColdSpare" + util::toString(m_id) + "_active");
	int failedPlaceID = doc->addPlace(0, 1, "ColdSpare" + util::toString(m_id) + "_failed");
	int failTransition = doc->addTimedTransition(m_failureRate);
	doc->transitionToPlace(activateTransition, activePlaceID);
	doc->placeToTransition(activePlaceID, failTransition);
	doc->transitionToPlace(failTransition, failedPlaceID);
	
	return make_pair(failedPlaceID, activateTransition);
}

FaultTreeNode* BasicEvent::clone() const
{
	return new BasicEvent(m_id, m_failureRate, m_name, m_cost);
}

std::string BasicEvent::description() const 
{
	return FaultTreeNode::description() 
		+ " Rate: " + util::toString(m_failureRate);
}