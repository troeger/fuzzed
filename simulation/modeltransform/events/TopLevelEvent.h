#pragma once
#include "Event.h"

class TopLevelEvent : public Event
{
public:
	TopLevelEvent(const std::string& ID);
	virtual ~TopLevelEvent() {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual void addChild(FaultTreeNode* child) override;
	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const override;

	virtual bool isValid() const override { return m_children.size() == 1; };

	virtual void print(std::ostream& stream, int indentLevel=0) const override;
};