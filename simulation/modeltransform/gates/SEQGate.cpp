#include "SEQGate.h"
#include "serialization/PNDocument.h"

SEQGate::SEQGate(int id, const std::vector<int>& ordering, const std::string& name /*= ""*/)
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
	for (const int& i : m_ordering)
	{
		FaultTreeNode* childNode = nullptr;
		for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		{
			if (childNode->getId() != i)
				continue;
		}
		
		if (!childNode)
			throw runtime_error("ID in sequence list was not among the children"); // TODO check this earlier

		int childFailed = childNode->serialize(doc);
		int propagateChildFailure = doc->addImmediateTransition();

		if (previousEvent > 0) // depend on the previous event happening
			doc->placeToTransition(previousEvent, propagateChildFailure);

		previousEvent = doc->addPlace(0);
		doc->placeToTransition(childFailed, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, previousEvent);
	}
}

