#include "FaultTreeNode.h"
#include "events/Event.h"
#include "serialization/PNDocument.h"
#include <typeinfo>
#include "util.h"

FaultTreeNode::FaultTreeNode(int ID, const std::string& name)
	: m_id(ID), m_name(name), m_parent(nullptr), m_cost(0)
{
}

void FaultTreeNode::addChild(FaultTreeNode* child)
{
	m_children.emplace_back(child);
	child->setParent(this);
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

FaultTreeNode* FaultTreeNode::getChildById(int id) 
{
	if (m_id == id)
		return this;

	for (auto& child : m_children)
	{
		if (child->getId() == id)
			return child;
		
		else 
		{
			FaultTreeNode* c = child->getChildById(id);
			if (c !=  nullptr)
				return c;
		}
	}
	return nullptr;
}

int FaultTreeNode::serialize(PNDocument* doc)
{
	return serialize(boost::shared_ptr<PNDocument>(doc));
}

string FaultTreeNode::description() const
{
	return 
		string(typeid(*this).name()) 
		+ " ID: " + util::toString(m_id)
		+ " NAME: " + m_name;
}

bool FaultTreeNode::addChildBelow(int id, FaultTreeNode* insertedChild)
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
	for (auto child : m_children)
	{
		delete child;
	}
}

const FaultTreeNode* FaultTreeNode::getRoot() const
{
	const FaultTreeNode* top = this;
	while (top->getParent() != nullptr)
		top = top->getParent();

	return top;
}

int FaultTreeNode::getCost() const
{
	int result = 0;
	for (auto& child : m_children)
	{
		result += child->getCost();
	}
	return result;
}
