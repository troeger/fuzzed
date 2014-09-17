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
    using namespace nodetype;
    return
        m_type == AND ||
        m_type == OR ||
        m_type == XOR ||
        m_type == VOTINGOR ||
        m_type == SPARE ||
        m_type == SEQ ||
        m_type == PAND;  
}

bool Node::isLeaf() const
{
    using namespace nodetype;
    return
        m_type == BASICEVENT ||
        m_type == UNDEVELOPEDEVENT ||
        m_type == HOUSEEVENT;
}

bool Node::isVariationPoint() const
{
    using namespace nodetype;
    return
        m_type == REDUNDANCYVP ||
        m_type == FEATUREVP;
}