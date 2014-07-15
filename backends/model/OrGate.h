#pragma once
#include "AbstractNode.h"

class BasicEvent : public AbstractNode
{
public:
	BasicEvent();

	virtual void toPetriNet(PetriNet* pn) override { /*TODO*/ };

protected:
	Probability m_probability;
};