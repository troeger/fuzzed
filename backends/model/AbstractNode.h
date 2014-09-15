#pragma once
#include <string>
#include <vector>

class PetriNet;

class AbstractNode
{
public:
	AbstractNode(const std::string id) : 
		m_id(id), m_optional(false), m_cost(1) {};
	virtual ~AbstractNode() {};

	virtual void addChild(AbstractNode* child) { m_children.emplace_back(child); };
	const std::vector<AbstractNode*>& children() const { return m_children; };

	virtual void toPetriNet(PetriNet* pn) = 0;

	virtual const std::string& getTypeDescriptor() const = 0;
	
	const std::string& getId()		{ return m_id; };
	const std::string& getName()	{ return m_name; };
	
	const unsigned int& getCost()	{ return m_cost; };
	const bool& isOptional()		{ return m_optional; };


protected:
	bool m_optional;
	unsigned int m_cost;

	std::string m_name;
	std::string m_id;

	std::vector<AbstractNode*> m_children;
};
