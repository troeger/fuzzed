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
	checkPlaceSequence(pn);
	return m_satisfied;
}

bool SequentialConstraint::checkPlaceSequence(const PetriNet* const pn)
{
	for (const auto& placeMarking : pn->m_placeDict)
	{
		if (placeMarking.second.getCurrentMarking() > 0)
		{
			const string& placeID = placeMarking.second.getID();
			for (unsigned int i = 0; i != m_sequencePos; ++i)
				if (m_requiredSequence.at(i) == placeID)
				{
					m_satisfied = false;
					return false;
				}

				for (unsigned int i = m_sequencePos; i != m_requiredSequence.size(); ++i)
					if (m_requiredSequence.at(i) == placeID)
						m_sequencePos = i;
		}
	}
	return true;
}

bool SequentialConstraint::checkTransitionSequence(const PetriNet* const pn)
{
	string current = m_requiredSequence.front();
	for (auto tt : pn->m_activeTimedTransitions)
	{ // find the currently required transition
		const string& transitionID = tt.second->getID();
		for (auto itFront : m_requiredSequence)
		{
			if (itFront == transitionID)
				return false;
		}
		for (auto itBack : m_requiredSequence)
		{
			if (itBack == transitionID)
			{
				current = itBack;
				break;
			}
		}
	}
	return true;
}