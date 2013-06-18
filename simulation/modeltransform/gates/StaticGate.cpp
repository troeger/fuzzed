#include "StaticGate.h"

StaticGate::StaticGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

long double StaticGate::computeUnreliability() const
{
	NodeValueMap unreliabilities;
	for (const FaultTreeNode* childNode : m_children)
	{
		const StaticGate* child = dynamic_cast<const StaticGate*>(childNode); // TODO compute with probabilities from basic events		
		unreliabilities.insert(std::make_pair(childNode->getId(), child ? child->computeUnreliability() : 1.0L));
	}
	return m_activationFunc(unreliabilities);
}