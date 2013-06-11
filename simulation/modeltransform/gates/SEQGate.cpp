#include "SEQGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"

using namespace std;

SEQGate::SEQGate(const string& id, const vector<string>& ordering, const string& name /*= ""*/)
	: PANDGate(id, ordering, name), m_ordering(ordering)
{}

FaultTreeNode* SEQGate::clone() const 
{
	SEQGate* cloned  = new SEQGate(m_id, m_ordering, m_name);
	for (auto& child : m_children)
		cloned->addChild(child->clone());

	return cloned;
}

int SEQGate::addSequenceViolatedPlace(boost::shared_ptr<PNDocument> doc) const 
{
	return doc->addPlace(0, 1, "SequenceViolated", CONSTRAINT_VIOLATED_PLACE);
}
