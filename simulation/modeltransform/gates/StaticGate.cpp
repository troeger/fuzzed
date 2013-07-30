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

int StaticGate::serializeTimeNet(std::shared_ptr<TNDocument> doc) const 
{
	assert(doc.get());

	std::string staticFormula = serializeAsFormula(doc);
	const int gateInput = doc->addPlace(1, 1);

	if (hasDynamicChildren())
		return serializePTNet(doc);
	
	const int fulfilFormula = doc->addGuardedTransition(staticFormula);
	const int gateFired = doc->addPlace(0, 1);

	doc->placeToTransition(gateInput, fulfilFormula);
	doc->transitionToPlace(fulfilFormula, gateFired);

	return gateFired;
}

bool StaticGate::hasDynamicChildren() const
{
	return !m_bStaticSubTree; // TODO
}

const std::string StaticGate::s_NOToperator = " NOT ";
const std::string StaticGate::s_ORoperator = " OR ";
const std::string StaticGate::s_ANDoperator = " AND ";
const std::string StaticGate::s_formulaBegin = "(";
const std::string StaticGate::s_formulaEnd = ")";