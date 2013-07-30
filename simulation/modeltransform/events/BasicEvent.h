#pragma once
#include "Event.h"

class BasicEvent : public Event
{
public:
	BasicEvent(const std::string& ID, long double failureRate, const std::string& name = "", const int cost = 1);
	
	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying

	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const override;
	
	std::pair<int /*placeID*/,int /*spareActivationTransition*/> 
		serializeAsColdSpare(std::shared_ptr<PNDocument> doc) const;

	std::tuple<int /*not failed*/, int /*failed*/, int /*failure transition*/>
		serializeAsSpare(std::shared_ptr<PNDocument> doc) const;

	virtual int getCost() const override { return m_cost; };

protected:
	void serializeFDEPChildren(std::shared_ptr<PNDocument> doc, const int& failedPlaceId) const;

	virtual std::string description() const override;
};