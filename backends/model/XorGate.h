#pragma once
#include "AbstractNode.h"

class XorGate : public AbstractNode
{
public:
    XorGate(const std::string id, const std::string name="") : AbstractNode(id, name) {};

    void toPetriNet(PetriNet* pn) override;
    const std::string& getTypeDescriptor() const override;

};