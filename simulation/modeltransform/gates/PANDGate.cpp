#include "PANDGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

PANDGate::PANDGate(const string& id, const std::vector<std::string>& ordering, const string& name/* = ""*/)
	: DynamicGate(id, name), m_requiredSequence(ordering)
{}


int PANDGate::serializePTNet(boost::shared_ptr<PNDocument> doc) const 
{
	// old version which discards invalid child sequences in a separate place
	// this is ugly modeling...

	int previousChildFailed = -1;
	int garbage = addSequenceViolatedPlace(doc);
	for (auto& child : m_children)
	{
		int childFailed = child->serializePTNet(doc);
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
	FaultTreeNode* newNode = new PANDGate(m_id, m_requiredSequence, m_name);
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

int PANDGate::serializeTimeNet(boost::shared_ptr<TNDocument> doc) const 
{
	// see: FuzzTrees / simulation / modeltransform / timeNetModels / PAND.xml
	
	vector<int> inhibitingPlaces;
	
	const int pandFailed = doc->addPlace(0);
	const int failPand = doc->addImmediateTransition();

	// fail just once
	doc->transitionToPlace(failPand, pandFailed);
	doc->addInhibitorArc(pandFailed, failPand);

	// TODO this can be optimized I suppose
	for (const auto& childId : m_requiredSequence)
	{
		const auto& child = getChildById(childId);
		assert(child != nullptr);

		const int childFailed				= child->serializeTimeNet(doc);
		const int propagateChildFailure		= doc->addImmediateTransition();
		const int childFailurePropagated	= doc->addPlace(0);

		doc->placeToTransition(childFailed, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, childFailed);

		doc->transitionToPlace(propagateChildFailure, childFailurePropagated);

		for (const auto& inhibitor : inhibitingPlaces)
			doc->addInhibitorArc(inhibitor, propagateChildFailure);

		inhibitingPlaces.emplace_back(childFailurePropagated);

		doc->placeToTransition(childFailurePropagated, failPand);
	}

	return pandFailed;
}
