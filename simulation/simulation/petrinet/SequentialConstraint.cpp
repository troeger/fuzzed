#include "SequentialConstraint.h"
#include "PetriNet.h"

using namespace std;

SequentialConstraint::SequentialConstraint(const vector<string>& sequence, SequenceType type) :
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
	auto sequencePos = m_requiredSequence.begin();
	for (const auto& p : pn->m_activeTimedTransitions)
	{
		const string transitionID = p.second->getID();
		for (auto it = m_requiredSequence.begin(); it != m_requiredSequence.end(); ++it)
		{ // find this transition
			if (it->getID() == transitionID)
			{
				if (sequencePos > it) return false;
				sequencePos = it;
			}
		}
	
	}
}