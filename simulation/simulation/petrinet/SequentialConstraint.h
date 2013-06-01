#pragma once
#include "PetriNetConstraint.h"
#include <vector>
#include <string>

class PetriNet;

enum SequenceType
{
	STATIC_TRANSITIION_SEQ,
	DYNAMIC_PLACE_SEQ
};

class SequentialConstraint
{
public:
	SequentialConstraint(const std::vector<std::string>& sequence, SequenceType type);
	bool isSatisfied(const PetriNet* const pn);

private:
	bool checkPlaceSequence(const PetriNet* const pn);
	bool checkTransitionSequence(const PetriNet* const pn);

	SequenceType m_type;
	std::vector<std::string> m_requiredSequence;
	int m_sequencePos;

	bool m_satisfied;
};
