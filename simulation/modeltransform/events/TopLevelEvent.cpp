#include "TopLevelEvent.h"
#include "serialization/PNDocument.h"
#include "util.h"
#include "gates/Gate.h"

TopLevelEvent::TopLevelEvent(const std::string& ID /*= 0*/)
	: Event(ID, 0.0L)
{}

int TopLevelEvent::serializePTNet(std::shared_ptr<PNDocument> doc) const 
{
	assert(m_children.size() <= 1 && "Top Level Event cannot have multiple children");
	
	int finalPlaceID = doc->addTopLevelPlace("SystemFailure");

	try
	{
		if (!m_children.empty())
		{
			FaultTreeNode* gate = m_children.front();
			int gatePlaceID = gate->serializePTNet(doc);
			int transitionID = doc->addImmediateTransition();

			doc->placeToTransition(gatePlaceID, transitionID);
			doc->transitionToPlace(transitionID, finalPlaceID);
		}
	}
	catch (exception& e)
	{
		cout << e.what() << endl;
	}
	
	return finalPlaceID;
}

void TopLevelEvent::addChild(FaultTreeNode* child)
{
	if (!m_children.empty())
	{
		OUTPUT("Replacing Gate below Top Level Event! Take care to add just one Gate!");
		m_children[0] = child;
	}
	else
	{
		m_children.push_back(child);
	}
	child->setParent(this);
}

FaultTreeNode* TopLevelEvent::clone() const
{
	FaultTreeNode* newNode = new TopLevelEvent(m_id);
	for (auto& child : m_children)
	{
		newNode->addChild(child->clone());
	}
	return newNode;
}

void TopLevelEvent::print(std::ostream& stream, int indentLevel/*=0*/) const 
{
	stream << "Fault Tree with Cost: " << getCost() << endl;
	FaultTreeNode::print(stream, indentLevel);
}

std::string TopLevelEvent::serializeAsFormula(std::shared_ptr<PNDocument> doc) const 
{
	assert(m_children.size() == 1);
	return m_children.front()->serializeAsFormula(doc);
}

int TopLevelEvent::serializeTimeNet(std::shared_ptr<TNDocument> doc) const 
{
	assert(m_children.size() <= 1 && "Top Level Event cannot have multiple children");

	int finalPlaceID = doc->addTopLevelPlace("SystemFailure");

	try
	{
		if (!m_children.empty())
		{
			FaultTreeNode* gate = m_children.front();
			int gatePlaceID = gate->serializeTimeNet(doc);
			int transitionID = doc->addImmediateTransition();

			doc->placeToTransition(gatePlaceID, transitionID);
			doc->transitionToPlace(transitionID, finalPlaceID);
		}
	}
	catch (exception& e)
	{
		cout << e.what() << endl;
	}

	return finalPlaceID;
}
