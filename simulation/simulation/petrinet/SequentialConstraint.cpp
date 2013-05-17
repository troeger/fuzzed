#include "SequentialConstraint.h"
#include "PetriNet.h"

using namespace std;

SequentialConstraint::SequentialConstraint(const vector<string>& sequence)
	: m_requiredSequence(sequence), 
	m_satisfied(true), 
	m_sequencePos(0)
{}

bool SequentialConstraint::isSatisfied(const PetriNet* const pn)
{
	assert(m_satisfied);
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