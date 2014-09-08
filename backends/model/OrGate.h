#pragma once
#include "AbstractNode.h"

class OrGate : public AbstractNode
{
public:
	OrGate(const std::string id) : AbstractNode(id) {};

	void toPetriNet(PetriNet* pn) override;
	const std::string& getTypeDescriptor() const override;

};