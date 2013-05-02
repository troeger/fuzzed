#include "PANDGate.h"
#include "serialization/PNDocument.h"
#include "events/BasicEvent.h"
#include "util.h"

PANDGate::PANDGate(int id, const std::set<int>& prioIds, const string& name/* = ""*/)
	: Gate(id, name), m_prioIDs(prioIds)
{
	m_bDynamic = true;
}


int PANDGate::serialize(boost::shared_ptr<PNDocument> doc) const 
{
	vector<int> priorityIds;
	vector<int> regularIds;
	for (auto it = getChildrenBegin(); it != getChildrenEnd(); ++it)
	{
		FaultTreeNode* node = dynamic_cast<FaultTreeNode*>(*it);
		if (CONTAINS(m_prioIDs, node->getId()))
			priorityIds.push_back(node->serialize(doc));
		else
			regularIds.push_back(node->serialize(doc));
	}

	int transitionID = doc->addImmediateTransition(2.0);
	for (int id : regularIds)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		doc->placeToTransition(id, transitionID);
	}

	for (int id : priorityIds)
	{
		if (id < 0)
		{
			cout << "Invalid child found, ID: " << id << endl;
			continue;
		}
		doc->placeToTransition(id, transitionID);

		int garbageTransition = doc->addImmediateTransition(1.0);
		int garbagePlace = doc->addPlace(0, 0, "PAND_Disabled", false);
		doc->placeToTransition(id, garbageTransition);
		doc->transitionToPlace(garbageTransition, garbagePlace, 0);
	}

	int placeID = doc->addPlace(0, 100, "PAND_Failed");
	doc->transitionToPlace(transitionID, placeID);

	cout << "Value of AND: " << getValue() << endl;

	return placeID;
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