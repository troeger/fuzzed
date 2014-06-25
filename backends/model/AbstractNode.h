#pragma once

class AbstractNode
{
public:
	AbstractNode(const std::string id) : m_id(id), m_optional(false), m_cost(1) {};
	virtual ~AbstractNode();

	virtual void addChild(AbstractNode* child) { m_children.emplace_back(child); };
	const std::vector<AbstractNode*>& children() const { return m_children; };

	virtual void toPetriNet(PetriNet* pn) override = 0;

protected:
	static std::string m_typeDescriptor = 0;

	bool m_optional;
	unsigned int m_cost;
	std::string m_id;

	std::vector<AbstractNode*> m_children;
};