#include "SEQGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"

using namespace std;

SEQGate::SEQGate(const string& id, const vector<string>& ordering, const string& name /*= ""*/)
	: PANDGate(id, ordering, name)
{}

FaultTreeNode::Ptr SEQGate::clone() const 
{
	auto cloned  = make_shared<SEQGate>(m_id, m_requiredSequence, m_name);
	for (auto& child : m_children)
		cloned->addChild(child->clone());

	return cloned;
}

int SEQGate::addSequenceViolatedPlace(std::shared_ptr<PNDocument> doc) const 
{
	return doc->addPlace(0, 1, "SequenceViolated", CONSTRAINT_VIOLATED_PLACE);
}
