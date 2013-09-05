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

int FDEPGate::serializeTimeNet(std::shared_ptr<TNDocument> doc) const 
{
	assert(getNumChildren() == 1);

	auto& trigger = m_children.front();
	if (trigger->getId() != m_triggerID)
		throw std::runtime_error("Trigger must be first and only child of FDEP");
	
	const int triggered = trigger->serializeTimeNet(doc);
	const int triggerTrans = doc->addImmediateTransition();
	doc->placeToTransition(triggered, triggerTrans);

	for (const auto& dependent : m_dependentEvents)
	{
		auto be = std::dynamic_pointer_cast<BasicEvent>(getChildById(dependent));
		if (!be)
			throw std::runtime_error("Dependent events must be BasicEvents");

		const int dependentEventOccured = be->serializeTimeNet(doc); // TODO: serialize just once!
		doc->transitionToPlace(triggerTrans, dependentEventOccured);
	}

	return -1; // FDEP gates do not propagate upwards
}
