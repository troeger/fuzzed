#include "BasicEvent.h"
#include "serialization/PNDocument.h"
#include "util.h"

BasicEvent::BasicEvent(const std::string& ID, long double failureRate, const std::string& name/* = ""*/, int cost /*=1*/)
	: Event(ID, failureRate, name)
{
	m_cost = cost;
}

int BasicEvent::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	int notFailed = doc->addPlace(1, 1, "BasicEvent" + m_id);
	int failComponent = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(notFailed, failComponent);
	
	int failed = doc->addPlace(0, 100, "BasicEvent" + m_id + "_occured");
	doc->transitionToPlace(failComponent, failed);
	return failed;
}

void BasicEvent::addChild(FaultTreeNode*)
{
	assert(false && "This is a leaf node!");
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

std::pair<int /*placeID*/,int /*spareActivationTransition*/> BasicEvent::serializeAsColdSpare(boost::shared_ptr<PNDocument> doc) const
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

	return make_pair(failedPlaceID, activateTransition);
}

std::pair<int /*placeID*/, int /*timedTransitionID*/> 
	BasicEvent::serializeSequential(boost::shared_ptr<PNDocument> doc) const
{
	int notFailed = doc->addPlace(1, 1, "BasicEvent" + m_id);
	int failComponent = doc->addTimedTransition(m_failureRate);
	doc->placeToTransition(notFailed, failComponent);

	int failed = doc->addPlace(0, 1, "BasicEvent" + m_id + "_occured");
	doc->transitionToPlace(failComponent, failed);
	return make_pair(failed, failComponent);
}