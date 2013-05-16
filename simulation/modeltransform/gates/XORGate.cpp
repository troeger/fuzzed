#include "XORGate.h"
#include "serialization/TimeNETDocument.h"

XORGate::XORGate(const std::string& ID, const std::string& name)
	: Gate(ID, name)
{}

int XORGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> childIDs;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
		childIDs.push_back((*it)->serialize(doc));

	int oneChildFailed			= doc->addPlace(0, 100, "XOR_Failed");
	int moreThanOneChildFailed	= doc->addPlace(0, 0, "XOR_moreThanOne");
	for (int id : childIDs)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		int propagateChildFailure = doc->addImmediateTransition();

		doc->placeToTransition(id, propagateChildFailure);
		doc->transitionToPlace(propagateChildFailure, oneChildFailed);
	}

	int discardMultipleFailures = doc->addImmediateTransition(2.0, Condition(), "more than one child failed");
	doc->placeToTransition(oneChildFailed, discardMultipleFailures, 2); // TODO: this should be ">=2". Or add transitions for everi i<numChildren.
	doc->transitionToPlace(discardMultipleFailures, moreThanOneChildFailed, 0);

	return oneChildFailed;
}