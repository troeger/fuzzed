#pragma once
#include "AbstractNode.h"

class EventSet : public AbstractNode
{
public:
	EventSet(const std::string id) : AbstractNode(id) {};
	const unsigned int& getQuantity()	{ return m_quantity; };
	
protected:
	unsigned int m_quantity;
};
