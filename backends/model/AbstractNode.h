#pragma once
#include <string>
#include <vector>

class PetriNet;

class AbstractNode
{
public:
	AbstractNode(const std::string id, const std::string typeDescriptor) : 
		m_id(id), m_optional(false), m_cost(1), m_typeDescriptor(typeDescriptor) {};
	virtual ~AbstractNode();

	virtual void addChild(AbstractNode* child) { m_children.emplace_back(child); };
	const std::vector<AbstractNode*>& children() const { return m_children; };

	virtual void toPetriNet(PetriNet* pn) = 0;

protected:
	const std::string m_typeDescriptor;

	bool m_optional;
	unsigned int m_cost;
	std::string m_id;

	std::vector<AbstractNode*> m_children;
};