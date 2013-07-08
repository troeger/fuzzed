#include "FDEPGate.h"
#include "serialization/PNDocument.h"

FDEPGate::FDEPGate(const std::string& id, const std::string& trigger, std::vector<std::string> dependentEvents, const std::string& name /*= ""*/)
	: DynamicGate(id, name), m_triggerID(trigger), m_dependentEvents(dependentEvents)
{}

int FDEPGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	int gateTriggered = doc->addPlace(0, 1, "FDEP triggered");

	assert(m_children.size() == 1); // this should be the triggering event
	int childTriggered = m_children.front()->serialize(doc);

	int triggerTrans = doc->addImmediateTransition();

	doc->placeToTransition(childTriggered, triggerTrans);
	doc->transitionToPlace(triggerTrans, gateTriggered);

	// TODO: find the dependent events' output places and connect to them...

	return gateTriggered;
}

FaultTreeNode* FDEPGate::clone() const 
{
	FaultTreeNode* newNode = new FDEPGate(m_id, m_triggerID, m_dependentEvents, m_name);
	for (auto& child : m_children)
		newNode->addChild(child->clone());

	return newNode;
}

