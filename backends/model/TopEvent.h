#pragma once
#include "AbstractNode.h"

class TopEvent : public AbstractNode
{
public:
	TopEvent(const std::string id) : Node(id) {};
	virtual ~TopEvent();

	virtual void addChild(Node* child) override
	{
		assert(m_children.empty() && "Top Events can only have one child");
		Node::addChild(child);
	};

protected:
	static std::string m_typeDescriptor = "topEvent";
};