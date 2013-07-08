#include "StaticGate.h"
#include "events/BasicEvent.h"

StaticGate::StaticGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

long double StaticGate::computeUnreliability() const
{
	NodeValueMap unreliabilities;
	for (const FaultTreeNode* childNode : m_children)
	{
		const StaticGate* child = dynamic_cast<const StaticGate*>(childNode);
		if (child)
			unreliabilities.insert(std::make_pair(childNode->getId(), child->computeUnreliability()));
		else
		{
			const BasicEvent* be = dynamic_cast<const BasicEvent*>(childNode);
			if (be)
				unreliabilities.insert(std::make_pair(childNode->getId(), be->getFailureRate()));
			else
				unreliabilities.insert(std::make_pair(childNode->getId(), 1.0L)); // TODO
		}
	}
	return m_activationFunc(unreliabilities);
}

const std::string StaticGate::s_NOToperator = " NOT ";
const std::string StaticGate::s_ORoperator = " OR ";
const std::string StaticGate::s_ANDoperator = " AND ";
const std::string StaticGate::s_formulaBegin = "(";
const std::string StaticGate::s_formulaEnd = ")";