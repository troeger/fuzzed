#include "Gate.h"

Gate::Gate(const std::string& ID, const std::string& name)
	: FaultTreeNode(ID, name), m_bDynamic(false)
{}

long double Gate::computeUnreliability() const
{
	NodeValueMap unreliabilities;
	for (const FaultTreeNode* childNode : m_children)
	{
		unreliabilities.insert(std::make_pair(childNode->getId(), childNode->getValue()));
	}
	return m_activationFunc(unreliabilities);
}

long double Gate::getValue() const
{
	if (m_bDynamic)
		return 1.0L;
	return computeUnreliability();
}
