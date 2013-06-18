#include "PANDGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

PANDGate::PANDGate(const string& id, const std::vector<std::string>& ordering, const string& name/* = ""*/)
	: DynamicGate(id, name), m_prioIDs(ordering)
{}


int PANDGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	int previousChildFailed = -1;
	int garbage = addSequenceViolatedPlace(doc);
	for (auto& child : m_children)
	{
		int childFailed = child->serialize(doc);
		if (previousChildFailed > 0)
		{
			int discard		= doc->addImmediateTransition(1, "discard");
			int propagate	= doc->addImmediateTransition(2, "propagate");

			doc->placeToTransition(previousChildFailed, propagate);
			doc->placeToTransition(childFailed, discard);
			doc->transitionToPlace(discard, garbage);

			int currentSequence = doc->addPlace(0, 1);
			doc->transitionToPlace(propagate, currentSequence);

			previousChildFailed = currentSequence;
		}
		else
		{
			previousChildFailed = childFailed;
		}
	}
	return previousChildFailed;
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
	return doc->addPlace(0, 0, "SequenceViolated");
}