#include "Transition.h"
#include <typeinfo>
#include "Place.h"
#include "util.h"

void Transition::fire()
{
	for (auto& p : m_inPlaces)
		p.first->consumeTokens(this, p.second);

	for (auto& p : m_outPlaces)
		p.first->produceTokens(p.second);

	m_hasNotFired = false;
}

bool Transition::wantsToFire(int tick)
{
	return 
		m_hasNotFired &&
		enoughTokens() &&
		stochasticallyEnabled(tick);
}

Transition::Transition(const string& id, const string& label /*= ""*/)
	: m_ID(id),
	m_label(label),
	m_hasNotFired(true),
	m_wasNotEnabled(true)
{}

Transition::Transition(const Transition& other)
	: m_inPlaces(PlaceTokenMap()),
	m_outPlaces(PlaceTokenMap()),
	m_ID(other.m_ID),
	m_label(other.m_label),
	m_hasNotFired(true),
	m_wasNotEnabled(true)
{}

void Transition::tryToFire()
{
	for (auto& p : m_inPlaces)
	{
		Place* const place = p.first;
		const int numTokens = p.second;

		assert(place->getCurrentMarking() >= numTokens);
		place->requestTokens(this);
	}
}

bool Transition::enoughTokens() const
{
	for (const auto& p : m_inPlaces)
	{
		if (p.first->getCurrentMarking() < p.second)
			return false;
	}
	for (const auto& p: m_inhibitingPlaces)
	{
		if (p.first->getCurrentMarking() > p.second)
			return false;
	}
	return true;
}

bool Transition::operator==(Transition const& lhs)
{
	return this->m_ID == lhs.m_ID;
}

void Transition::addInPlace(Place* p, const unsigned int& numTokens)
{
	m_inPlaces[p] = numTokens;
}


void Transition::addInhibitingPlace(Place* p, const unsigned int& numTokens)
{
	m_inhibitingPlaces[p] = numTokens;
}


void Transition::addOutPlace(Place* p, const unsigned int& numTokens)
{
	m_outPlaces[p] = numTokens;
}

void Transition::removeInPlace(Place* p)
{
	m_inPlaces.erase(p);
}

void Transition::removeOutPlace(Place* p)
{
	m_outPlaces.erase(p);
}

void Transition::reset()
{
	m_hasNotFired = true;
	m_wasNotEnabled = true;
}
