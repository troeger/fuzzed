#include "Node.h"

bool Node::isEvent() const
{
    using namespace nodetype;
    return
        m_type == BASICEVENT ||
        m_type == TOPEVENT ||
        m_type == UNDEVELOPEDEVENT ||
        m_type == INTERMEDIATEEVENT;
}

bool Node::isGate() const
{
    return false;   
}

bool Node::isLeaf() const
{
    return false;
}

bool Node::isVariationPoint() const
{
    return false;
}