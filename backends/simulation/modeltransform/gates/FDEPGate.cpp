#include "FDEPGate.h"
#include "events/BasicEvent.h"
#include "serialization/PNDocument.h"

#include <stdexcept>

FDEPGate::FDEPGate(const std::string& id, const std::string& trigger, std::vector<std::string> dependentEvents, const std::string& name /*= ""*/)
	: DynamicGate(id, name), m_triggerID(trigger), m_dependentEvents(dependentEvents)
{}

int FDEPGate::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	const auto& triggerChild = getChildById(m_triggerID);
	return triggerChild->serializePTNet(doc); // FDEP gates do not propagate upwards
}

FaultTreeNode::Ptr FDEPGate::clone() const 
{
	FaultTreeNode::Ptr newNode = std::make_shared<FDEPGate>(m_id, m_triggerID, m_dependentEvents, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}
