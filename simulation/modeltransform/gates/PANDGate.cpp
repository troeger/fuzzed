#include "PANDGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

PANDGate::PANDGate(const string& id, const std::vector<std::string>& ordering, const string& name/* = ""*/)
	: Gate(id, name), m_prioIDs(ordering)
{
	m_bDynamic = true;
}


int PANDGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	// TODO
	return -1;
}

FaultTreeNode* PANDGate::clone() const
{
	FaultTreeNode* newNode = new PANDGate(m_id, m_prioIDs, m_name);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}

int PANDGate::addSequenceViolatedPlace(boost::shared_ptr<PNDocument> doc) const
{
	return doc->addPlace(0, 0, "SequenceViolated", false);
}