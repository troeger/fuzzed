#pragma once
#include <string>
#include <vector>

class PetriNet;

class AbstractNode
{
public:
	AbstractNode(const std::string id) : 
		m_id(id), m_optional(false), m_cost(1) {};
	virtual ~AbstractNode();

	virtual void addChild(AbstractNode* child) { m_children.emplace_back(child); };
	const std::vector<AbstractNode*>& children() const { return m_children; };

	virtual void toPetriNet(PetriNet* pn) = 0;

	virtual const std::string& getTypeDescriptor() = 0;
	
	const std::string& getId() { return m_id; };


protected:
	bool m_optional;
	unsigned int m_cost;
	std::string m_id;

	std::vector<AbstractNode*> m_children;
};
