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

Place::Place(const string& id, int initialMarking, int capacity, PlaceSemantics semantics) :
	m_initialMarking(initialMarking),
	m_marking(initialMarking), 
	m_ID(id), 
	m_capacity(capacity), 
	m_semantics(semantics), 
	m_transitionQueue(set<Transition*>())
{
	if (m_capacity > 0 && m_capacity < m_marking)
		throw runtime_error("Invalid Place configuration: the initial marking must not be larger than capacity.");
}

Place::Place(const Place& other) :
	m_initialMarking(other.m_initialMarking),
	m_marking(other.m_initialMarking),
	m_capacity(other.m_capacity),
	m_ID(other.m_ID),
	m_semantics(other.m_semantics),
	m_transitionQueue(set<Transition*>())
{
	if (m_capacity > 0 && m_capacity < m_marking)
		throw runtime_error("Invalid Place configuration: the initial marking must not be larger than capacity.");
}

Place::Place() : m_initialMarking(0), m_capacity(0), m_marking(0)
{
	assert(false);
}

void Place::resolveConflictsTimed(int)
{
	assert(m_marking >= 0);
	assert(hasRequests());

	// always take the first transition.
	// this is not strictly correct. TODO implement arbitrary precision random numbers or something
	TimedTransition* tt = dynamic_cast<TimedTransition*>(*m_transitionQueue.begin());
	tt->fire();
	m_transitionQueue.clear();
}

void Place::resolveConflictsImmediate(int tick)
{
	assert(m_marking >= 0);
	assert(hasRequests());

	// TODO handle weights?

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

	maxPrioIT->fire();
	m_transitionQueue.erase(maxPrioIT);
}

void Place::produceTokens(int numTokens)
{
	m_marking += numTokens;
	if (m_marking > m_capacity)
		m_marking = m_capacity;
}

void Place::reset()
{
	m_marking = m_initialMarking;
	m_transitionQueue.clear();
}