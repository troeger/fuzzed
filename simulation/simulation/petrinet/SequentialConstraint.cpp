#include "SequentialConstraint.h"
#include "PetriNet.h"

using namespace std;

SequentialConstraint::SequentialConstraint(const vector<string>& sequence, SequenceType type) :
	PetriNetConstraint(),
	m_requiredSequence(sequence),
	m_type(type),
	m_satisfied(true), 
	m_sequencePos(0)
{}

bool SequentialConstraint::isSatisfied(const PetriNet* const pn)
{
	assert(m_satisfied);

	switch (m_type)
	{
	case STATIC_TRANSITIION_SEQ: 
		return checkTransitionSequence(pn); 
	case DYNAMIC_PLACE_SEQ:
		return checkPlaceSequence(pn);
	default:
		assert(false);
	}

	return checkPlaceSequence(pn);
}

bool SequentialConstraint::checkPlaceSequence(const PetriNet* const pn)
{
	for (const auto& placeMarking : pn->m_placeDict)
	{
		if (placeMarking.second.getCurrentMarking() > 0)
		{
			const string placeID = placeMarking.second.getID();
			for (int i = 0; i != m_sequencePos; ++i)
				if (m_requiredSequence.at(i) == placeID)
				{
					m_satisfied = false;
					return false;
				}

				for (int i = m_sequencePos; i != m_requiredSequence.size(); ++i)
					if (m_requiredSequence.at(i) == placeID)
						m_sequencePos = i;
		}
	}
	return true;
}

bool SequentialConstraint::checkTransitionSequence(const PetriNet* const pn)
{
	unsigned int sequencePos = 0;

	auto current = m_requiredSequence.begin();
	for (auto tt = pn->m_activeTimedTransitions.begin(); tt != pn->m_activeTimedTransitions.end(); ++tt)
	{ // find the currently required transition
		const string transitionID = tt->second->getID();
		for (auto itFront = m_requiredSequence.begin(); itFront != current; ++itFront)
		{
			if (*itFront == transitionID)
				return false;
		}
		for (auto itBack = current; itBack != m_requiredSequence.end(); ++itBack)
		{
			if (*itBack == transitionID)
			{
				current = itBack;
				break;
			}
		}
	}
	return true;
}