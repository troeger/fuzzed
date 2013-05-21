#pragma once
#include "PetriNetConstraint.h"
#include <vector>
#include <string>

class SequentialConstraint
{
public:
	SequentialConstraint(const std::vector<std::string>& sequence);
	bool isSatisfied(const PetriNet* const pn);

private:
	std::vector<std::string> m_requiredSequence;
	int m_sequencePos;

	bool m_satisfied;
};
