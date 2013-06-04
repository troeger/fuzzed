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
	m_hasNotFired(true)
{}

Transition::Transition(const Transition& other)
	: m_inPlaces(PlaceTokenMap()),
	m_outPlaces(PlaceTokenMap()),
	m_ID(other.m_ID),
	m_label(other.m_label),
	m_hasNotFired(true)
{

}

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
		const unsigned int currentMarking = p.first->getCurrentMarking();
		assert(currentMarking >= 0);
		if (currentMarking < p.second)
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
