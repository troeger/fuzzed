#pragma once
#include "AbstractNode.h"

class VotingOrGate : public AbstractNode
{
public:
	VotingOrGate(const std::string id) : AbstractNode(id) {};

	void toPetriNet(PetriNet* pn) override;
	const std::string& getTypeDescriptor() const override;

};