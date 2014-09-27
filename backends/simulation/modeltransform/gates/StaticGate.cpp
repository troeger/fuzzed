#include "StaticGate.h"
#include "events/BasicEvent.h"

using std::dynamic_pointer_cast;

StaticGate::StaticGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

double StaticGate::computeUnreliability() const
{
	NodeValueMap unreliabilities;
	for (const FaultTreeNode::Ptr childNode : m_children)
	{
		auto child = dynamic_pointer_cast<StaticGate>(childNode);
		if (child)
			unreliabilities.insert(std::make_pair(childNode->getId(), child->computeUnreliability()));
		else
		{
			auto be = dynamic_pointer_cast<BasicEvent>(childNode);
			if (be)
				unreliabilities.insert(std::make_pair(childNode->getId(), be->getFailureRate()));
			else
				unreliabilities.insert(std::make_pair(childNode->getId(), 1.0L)); // TODO
		}
	}
	return m_activationFunc(unreliabilities);
}

bool StaticGate::hasDynamicChildren() const
{
	return !m_bStaticSubTree;
}

const std::string StaticGate::s_NOToperator = " NOT ";
const std::string StaticGate::s_ORoperator = " OR ";
const std::string StaticGate::s_ANDoperator = " AND ";
const std::string StaticGate::s_formulaBegin = "(";
const std::string StaticGate::s_formulaEnd = ")";