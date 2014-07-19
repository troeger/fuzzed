#pragma once
#include "AbstractNode.h"

class AndGate : public AbstractNode
{
public:
	AndGate(const std::string id) : AbstractNode(id) {};

	void toPetriNet(PetriNet* pn) override { /*TODO*/ };
	const std::string& getTypeDescriptor() override;
};