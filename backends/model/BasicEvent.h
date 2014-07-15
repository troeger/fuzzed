#pragma once
#include "AbstractNode.h"

class BasicEvent : public AbstractNode
{
public:
	BasicEvent(const std::string id) : AbstractNode(id, "basicEvent") {};

	virtual void toPetriNet(PetriNet* pn) override { /*TODO*/ };

protected:
	Probability m_probability;
};