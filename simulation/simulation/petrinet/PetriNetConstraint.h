#pragma once

class PetriNet;

enum ViolationConsequence
{
	ENFORCE_CONSTRAINT,
	REJECT_PETRINET
};

class PetriNetConstraint
{
public:
	PetriNetConstraint() : m_consequence(REJECT_PETRINET) {}
	virtual bool isSatisfied(const PetriNet* const) { return false; };

protected:
	ViolationConsequence m_consequence;
};