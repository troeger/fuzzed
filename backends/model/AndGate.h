#pragma once
#include "AbstractNode.h"

class AndGate : public AbstractNode
{
public:
	AndGate(const std::string id) : AbstractNode(id) {};

	void toPetriNet(PetriNet* pn) override;
	const std::string& getTypeDescriptor() const override;
};