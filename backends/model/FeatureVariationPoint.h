#pragma once
#include "AbstractNode.h"
#include <cassert>

class FeatureVariationPoint : public AbstractNode
{
public:
    virtual void toPetriNet(PetriNet* pn) override { assert(false); };
    virtual const std::string& getTypeDescriptor() const override
    {
        static const std::string str = "redundancyVariationPoint";
        return str;
    };
};