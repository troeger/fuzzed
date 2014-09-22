#pragma once
#include "Event.h"
#include <utility>
#include <tuple>

class BasicEvent : public Event
{
public:
	typedef std::tuple<int /*not failed*/, int /*failed*/, int /*failure transition*/> PNSpec;
	typedef std::pair<int /*placeID*/,int /*spareActivationTransition*/> PNSpareSpec;

	BasicEvent(const std::string& ID, double failureRate, const std::string& name = "", const int cost = 1);
	
	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying

	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const override;
	
	PNSpareSpec serializeAsColdSpare(std::shared_ptr<PNDocument> doc) const;
	PNSpec serializeAsSpare(std::shared_ptr<PNDocument> doc) const;

	virtual int getCost() const override { return m_cost; };

protected:
	void serializeFDEPChildren(std::shared_ptr<PNDocument> doc, const int& failedPlaceId) const;

	virtual std::string description() const override;

	mutable int m_serializedPlaceID;
};