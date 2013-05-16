#pragma once
#include "PetriNetConstraint.h"
#include <vector>

class SequentialConstraint
{
public:
	SequentialConstraint(const std::vector<std::string>& sequence);
	bool isSatisfied(const PetriNet* const pn) const;

private:
	std::vector<std::string> m_timedTransitionSequence;
};