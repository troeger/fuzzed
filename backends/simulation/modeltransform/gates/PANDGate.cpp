#include "PANDGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

PANDGate::PANDGate(const string& id, const std::vector<std::string>& ordering, const string& name/* = ""*/)
	: DynamicGate(id, name), m_requiredSequence(ordering)
{}


int PANDGate::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	// see: FuzzTrees / simulation / modeltransform / timeNetModels / PAND.xml

	vector<int> inhibitingPlaces;

	const int pandFailed = addSequenceViolatedPlace(doc);// doc->addPlace(0, 1);
	const int failPand = doc->addImmediateTransition();

	// fail just once
	doc->transitionToPlace(failPand, pandFailed);
	doc->addInhibitorArc(pandFailed, failPand);

	// TODO this can be optimized I suppose
	for (const auto& childId : m_requiredSequence)
	{
		const auto& child = getChildById(childId);
		assert(child != nullptr);

		const int childFailed				= child->serializePTNet(doc);
		const int propagateChildFailure		= doc->addImmediateTransition();
		const int childFailurePropagated	= doc->addPlace(0, 1);

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

FaultTreeNode::Ptr PANDGate::clone() const
{
	FaultTreeNode::Ptr newNode = std::make_shared<PANDGate>(m_id, m_requiredSequence, m_name);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}

int PANDGate::addSequenceViolatedPlace(std::shared_ptr<PNDocument> doc) const
{
	return doc->addPlace(0, 1, "SequenceViolated");
}

