#pragma once
#include "AbstractNode.h"
#include <cassert>

class RedundancyVariationPoint : public AbstractNode
{
public:
    virtual void toPetriNet(PetriNet* pn) override { assert(false); };
    virtual const std::string& getTypeDescriptor() const override
    {
        static const std::string str = "redundancyVariationPoint";
        return str;
    };

    const unsigned int& start() const { return m_start; }
    const unsigned int& end()   const { return m_end; }

    const std::string& formula() const { return m_formula; }

private:
    unsigned int m_start;
    unsigned int m_end;
    std::string m_formula;
};