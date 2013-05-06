#include "FDEPGate.h"
#include "serialization/PNDocument.h"

FDEPGate::FDEPGate(const std::string& id, int trigger, std::vector<const std::string> dependentEvents, const std::string& name /*= ""*/)
	: Gate(id, name), m_triggerID(trigger), m_dependentEvents(dependentEvents)
{
	m_bDynamic = true;
}

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

