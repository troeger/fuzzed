#include "SequentialConstraint.h"
#include "PetriNet.h"

using namespace std;

SequentialConstraint::SequentialConstraint(const vector<string>& sequence)
	: m_timedTransitionSequence(sequence)
{}

bool SequentialConstraint::isSatisfied(const PetriNet* const pn) const
{
	vector<string>::const_iterator sequencePtr = m_timedTransitionSequence.begin();
	for (const auto& timeTransitionPair : pn->m_activeTimedTransitions)
	{
		const string transitionID = timeTransitionPair.second->getID();
		for (auto it = m_timedTransitionSequence.begin(); it != sequencePtr; ++it)
			if (transitionID == *it) return false;

		for (auto it = sequencePtr; it != m_timedTransitionSequence.end(); ++it)
			if (*it == transitionID) sequencePtr = it;
	}
	return true;
}