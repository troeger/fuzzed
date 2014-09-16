#pragma once
#include "AbstractNode.h"
#include <pugixml.hpp>

class AbstractProbability;

class BasicEvent : public AbstractNode
{
public:
	BasicEvent(const std::string id, const std::string name="") : AbstractNode(id, name) {};

	virtual void toPetriNet(PetriNet* pn) override { /*TODO*/ };
	virtual const std::string& getTypeDescriptor() const override;

	void setProbability(const pugi::xml_node& probabilityNode);

protected:
	AbstractProbability* m_probability;
};