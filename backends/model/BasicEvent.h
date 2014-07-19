#pragma once
#include "AbstractNode.h"
#include <pugixml.hpp>

class AbstractProbability;

class BasicEvent : public AbstractNode
{
public:
	BasicEvent(const std::string id) : AbstractNode(id) {};

	virtual void toPetriNet(PetriNet* pn) override { /*TODO*/ };
	virtual const std::string& getTypeDescriptor();

	void setProbability(const pugi::xml_node& probabilityNode);

protected:
	AbstractProbability* m_probability;
};