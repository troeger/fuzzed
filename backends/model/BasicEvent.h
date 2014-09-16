#pragma once
#include "AbstractNode.h"
#include "AbstractProbability.h"
#include <pugixml.hpp>

class BasicEvent : public AbstractNode
{
public:
	BasicEvent(const std::string id, const std::string name="") : AbstractNode(id, name) {};
    BasicEvent(const BasicEvent& other) : AbstractNode(other.m_id, other.m_name), m_probability(other.m_probability) {};

	virtual void toPetriNet(PetriNet* pn) override { /*TODO*/ };
	virtual const std::string& getTypeDescriptor() const override;

    const AbstractProbability& getProbability() const { return m_probability; }

	void setProbabilityFromXml(const pugi::xml_node& probabilityNode);

protected:
	AbstractProbability m_probability;
};