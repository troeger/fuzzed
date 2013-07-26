#pragma once
#include "Event.h"

class BasicEvent : public Event
{
public:
	BasicEvent(const std::string& ID, long double failureRate, const std::string& name = "", const int cost = 1);
	
	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual void addChild(FaultTreeNode* child) override;
	
	virtual int serializePTNet(boost::shared_ptr<PNDocument> doc) const override;
	
	std::pair<int /*placeID*/,int /*spareActivationTransition*/> 
		serializeAsColdSpare(boost::shared_ptr<PNDocument> doc) const;

	std::tuple<int /*not failed*/, int /*failed*/, int /*failure transition*/>
		serializeAsSpare(boost::shared_ptr<PNDocument> doc) const;

	virtual int getCost() const override { return m_cost; };

protected:
	virtual std::string description() const override;
};