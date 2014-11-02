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
        m_type == HOUSEEVENT ||
        m_type == BASICEVENTSET ||
        m_type == INTERMEDIATEEVENTSET;
}

bool Node::isVariationPoint() const
{
    using namespace nodetype;
    return
        m_type == REDUNDANCYVP ||
        m_type == FEATUREVP;
}

bool Node::isEventSet() const
{
    using namespace nodetype;
    return
        m_type == BASICEVENTSET ||
        m_type == INTERMEDIATEEVENTSET;
}

bool Node::canHaveProbability() const
{
	using namespace nodetype;
	return
		m_type == BASICEVENTSET ||
		m_type == BASICEVENT;
}

bool Node::canHaveCost() const
{
	using namespace nodetype;
	return
		m_type == BASICEVENT ||
		m_type == BASICEVENTSET ||
		m_type == INTERMEDIATEEVENT ||
		m_type == INTERMEDIATEEVENTSET;
}

void Node::setProbabilityFromString(const std::string& str, const unsigned int missionTime)
{
	assert(canHaveProbability());
	m_probability = Probability::fromDescriptionString(str, missionTime);
}

const Probability& Node::getProbability() const
{
	assert(canHaveProbability());
	return m_probability;
}

void Node::setProbability(const Probability& p)
{
	assert(canHaveProbability());
	m_probability = p;
}


