#pragma once
#include "AbstractNode.h"

class OrGate : public AbstractNode
{
public:
	OrGate(const std::string id, const std::string name="") : AbstractNode(id, name) {};

	void toPetriNet(PetriNet* pn) override;
	const std::string& getTypeDescriptor() const override;

};