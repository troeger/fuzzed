#include "FaultTreeNode.h"
#include "events/Event.h"
#include "serialization/PNDocument.h"
#include <typeinfo>
#include <iostream>
#include "util.h"

FaultTreeNode::FaultTreeNode(const std::string& ID, const std::string& name)
	: m_id(ID), m_name(name), m_parent(nullptr), m_cost(0), m_bDynamic(false), m_bStaticSubTree(true)
{}

void FaultTreeNode::addChild(FaultTreeNode::Ptr child)
{
	m_children.emplace_back(child);
	child->setParent(this);

	if (child->m_bDynamic) markDynamic();
}

void FaultTreeNode::print(std::ostream& stream, int indentLevel) const
{
	int i=0;
	while (i++ < indentLevel)
		stream << "--";

	stream 
		<< description() 
		<< std::endl;
	
	++indentLevel;
	for (auto& child : m_children)
	{
		child->print(stream, indentLevel);	
	}
}

FaultTreeNode::Ptr FaultTreeNode::getChildById(const std::string& id) 
{
	// if (m_id == id) return this;

	for (auto& child : m_children)
	{
		if (child->getId() == id) return child;
		
		else 
		{
			FaultTreeNode::Ptr c = child->getChildById(id);
			if (c !=  nullptr) return c;
		}
	}
	return nullptr;
}


const FaultTreeNode::Ptr FaultTreeNode::getChildById(const std::string& id) const
{
	// if (m_id == id) return this;

	for (auto& child : m_children)
	{
		if (child->getId() == id) return child;

		else 
		{
			FaultTreeNode::Ptr c = child->getChildById(id);
			if (c !=  nullptr) return c;
		}
	}
	return nullptr;
}

string FaultTreeNode::description() const
{
	return 
		string(typeid(*this).name()) 
		+ " ID: " + m_id
		+ " NAME: " + m_name
		+ " S: " + (m_bStaticSubTree ? "y" : "n");
}

bool FaultTreeNode::addChildBelow(const std::string& id, FaultTreeNode::Ptr insertedChild)
{
	for (auto& child : m_children)
	{
		if (child->getId() == id)
		{
			child->addChild(insertedChild);
			return true;
		}

		else if (child->addChildBelow(id, insertedChild))
		{
			return true;
		}
	}
	return false;
}

FaultTreeNode::~FaultTreeNode()
{
// 	for (const auto& child : m_children)
// 		delete child;
}

const FaultTreeNode* FaultTreeNode::getRoot() const
{
	auto top = getParent();
	while (top && top->getParent())
		top = top->getParent();

	return top;
}

int FaultTreeNode::getCost() const
{
	int result = 0;
	for (auto& child : m_children)
		result += child->getCost();
	return result;
}

int FaultTreeNode::serializeTimeNet(std::shared_ptr<TNDocument> doc) const
{
	return serializePTNet(doc);
}

void FaultTreeNode::markDynamic()
{
	m_bStaticSubTree = false;
	if (m_parent)
		m_parent->markDynamic();
}

const FaultTreeNode* FaultTreeNode::getParent() const
{
	return m_parent;
}
