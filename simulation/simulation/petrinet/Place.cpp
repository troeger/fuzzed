#include "Place.h"
#include "TimedTransition.h"
#include "ImmediateTransition.h"
#include "implementation/Simulation.h"
#include <iostream>

void Place::consumeTokens(Transition* const t, int numTokens)
{
	if (m_transitionQueue.empty())
	{
		// TODO find out if this is legitimate
		return;
	}
	assert(m_transitionQueue.find(t) != m_transitionQueue.end());
	assert(m_marking >= numTokens);
	
	m_marking -= numTokens;

	if (m_marking == 0)
		m_transitionQueue.clear();
}

void Place::requestTokens(Transition* const t)
{
	m_transitionQueue.insert(t);
}

Place::Place(const string& id, int initialMarking, int capacity, bool isTopLevel) :
	m_marking(initialMarking), 
	m_ID(id), 
	m_capacity(capacity), 
	m_bTopLevelPlace(isTopLevel), 
	m_transitionQueue(set<Transition*>())
{
	if (m_capacity > 0 && m_capacity < m_marking)
		throw runtime_error("Invalid Place configuration: the initial marking must not be larger than capacity.");
}

Place::Place(const Place& other) :
	m_marking(other.m_marking),
	m_capacity(other.m_capacity),
	m_ID(other.m_ID),
	m_bTopLevelPlace(other.m_bTopLevelPlace),
	m_transitionQueue(set<Transition*>())
{
	if (m_capacity > 0 && m_capacity < m_marking)
		throw runtime_error("Invalid Place configuration: the initial marking must not be larger than capacity.");
}

void Place::resolveConflictsTimed(int tick)
{
	assert(m_marking >= 0);
	assert(hasRequests());

	double sumLambda = 0.0;
	for (Transition* t : m_transitionQueue)
	{
		TimedTransition* tt = dynamic_cast<TimedTransition*>(t);
		assert(tt && "At this stage only timed transitions should request a token");

		sumLambda += tt->getRate();
	}

	double r = m_gen.randomNumberInInterval(0.0, sumLambda);

	// for exponential distributions: P(i) = lambda_i/sumLambda
	// divide [0, sumLambda] into intervals corresponding to the transition probabilities
	// EXAMPLE: rates are (0.4, 0.5, 0.1)
	// sumLambda = 1.0
	// P(1) = 0.4/1.0 --> subinterval [0, 0.4]
	// P(2) = 0.5/1.0 --> subinterval [0.4, 0.9]
	// P(3) = 0.1/1.0 --> subinterval [0.9, 1.0]
	
	for (Transition* t : m_transitionQueue)
	{
		TimedTransition* tt = dynamic_cast<TimedTransition*>(t);
		assert(tt != nullptr);

		double lower = 0.0;
		double upper = lower + tt->getRate();
		if (r >= lower && r < upper)
		{
			tt->fire(tick);
			m_transitionQueue.erase(tt);
			return;
		}
		lower = upper;
	}
	assert(false && "One interval should have been chosen");
}

void Place::resolveConflictsImmediate(int tick)
{
	assert(m_marking >= 0);
	assert(hasRequests());

	ImmediateTransition* maxPrioIT = nullptr;
	for (auto i = m_transitionQueue.begin(); i != m_transitionQueue.end(); )
	{
		ImmediateTransition* it = dynamic_cast<ImmediateTransition*>(*i);
		assert(it && "At this stage only immediate transitions should request a token");

		const bool invalidated = !it->wantsToFire(tick);
		// find the highest priority transition
		// need to check if the transition wants to fire here, in case it fired already
		// this can occur if it has multiple in places one of which has multiple tokens
		if ((!maxPrioIT || it->getPriority() > maxPrioIT->getPriority()) && !invalidated)
			maxPrioIT = it;

		if (!invalidated)
			++i;
		else
			m_transitionQueue.erase(i++);
	}
	
	if (!maxPrioIT)
		return;

	maxPrioIT->fire(tick);
	m_transitionQueue.erase(maxPrioIT);
}

void Place::produceTokens(int numTokens)
{
	assert(m_marking+numTokens <= m_capacity);
	m_marking += numTokens;
}

Place& Place::operator=(const Place& other)
{
	m_marking = other.m_marking;
	m_capacity = other.m_capacity;
	m_ID = other.m_ID;
	m_bTopLevelPlace = other.m_bTopLevelPlace;
	m_transitionQueue = set<Transition*>();

	return *this;
}
