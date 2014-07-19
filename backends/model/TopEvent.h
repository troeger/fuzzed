#pragma once
#include "AbstractNode.h"
#include <cassert>

class TopEvent : public AbstractNode
{
public:
	TopEvent(const std::string id) : AbstractNode(id) {};
	virtual ~TopEvent();

	virtual void addChild(AbstractNode* child) override
	{
		assert(m_children.empty() && "Top Events can only have one child");
		AbstractNode::addChild(child);
	};


	virtual void toPetriNet(PetriNet* pn) override;

	virtual const std::string& getTypeDescriptor();

protected:
};
