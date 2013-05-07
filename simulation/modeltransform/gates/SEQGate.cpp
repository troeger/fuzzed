#include "SEQGate.h"
#include "serialization/PNDocument.h"

SEQGate::SEQGate(const string& id, const vector<string>& ordering, const string& name /*= ""*/)
	: Gate(id, name), m_ordering(ordering)
{}

FaultTreeNode* SEQGate::clone() const 
{
	SEQGate* cloned  = new SEQGate(m_id, m_ordering, m_name);
	for (auto& child : m_children)
		cloned->addChild(child->clone());

	return cloned;
}

int SEQGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	int previousEvent = -1;
	for (const string& i : m_ordering)
	{
		FaultTreeNode* childNode = nullptr;
		for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		{
			if ((*it)->getId() == i)
			{
				childNode = *it;
				break;
			}
		}
		
		if (!childNode)
			throw runtime_error("ID in sequence list was not among the children" + i); // TODO check this earlier

		int childFailed = childNode->serialize(doc);
		int propagateChildFailure = doc->addImmediateTransition(2.0);

		if (previousEvent > 0) // depend on the previous event happening
		{
			doc->placeToTransition(previousEvent, propagateChildFailure);
			// if the required previous event didn't happen before, trash the token
			int garbage = doc->addPlace(0, 0, "Discarded Sequence");
			int discard = doc->addImmediateTransition(1.0);
			doc->transitionToPlace(discard, garbage, 0);
			doc->placeToTransition(childFailed, discard);
		}
		previousEvent = doc->addPlace(0);
		doc->placeToTransition(childFailed, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, previousEvent);
	}
	return previousEvent;
}