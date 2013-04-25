#pragma once
#include "Event.h"

class BasicEvent : public Event
{
public:
	BasicEvent(int ID, long double failureRate, const std::string& name = "", const int cost = 1);
	virtual ~BasicEvent();

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual void addChild(FaultTreeNode* child) override;
	
	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
	
	std::pair<int /*placeID*/,int /*spareActivationTransition*/> 
		serializeAsColdSpare(boost::shared_ptr<PNDocument> doc) const;

	virtual int getCost() const override { return m_cost; };

protected:
	virtual std::string description() const override;
};