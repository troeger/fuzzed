#include "Transition.h"
#include <typeinfo>
#include "Place.h"
#include "util.h"

void Transition::fire(int tick)
{
	// cout << "Firing: " << m_ID << endl;
	m_active = false;

	if (m_bLoggingActive)
	{
		(*m_log) << 
			"FIRING at time " << util::toString(tick) << 
			" : " << typeid(*this).name() << " " <<  m_ID.c_str() << endl;
	}

	for (auto& p : m_inPlaces)
	{
		Place* const place = p.first;
		place->consumeTokens(this, p.second);
		if (m_bLoggingActive)
			(*m_log) << "--" << place->getID().c_str() << endl;
	}
	for (auto& p : m_outPlaces)
	{
		Place* const place = p.first;
		place->produceTokens(p.second);
		if (m_bLoggingActive)
			(*m_log) << "++" << place->getID().c_str() << endl;
	}
}

bool Transition::wantsToFire(int tick)
{
	if (!m_active)
		return false;

	for (const auto& p : m_inPlaces)
	{
		const int currentMarking = p.first->getCurrentMarking();
		assert(currentMarking >= 0);
		if (currentMarking < p.second)
			return false;
	}

	if (!m_enabled)
	{ 
		// the transition only just got enabled.
		// save the time, so it can be used to offset probability distribution.
		m_startupTime = tick;
	}

	bool result = stochasticallyEnabled(tick);
	if (!result)
		return false;

	return true;
}

Transition::Transition(const string& id)
	: m_ID(id),
	m_bLoggingActive(false),
	m_active(true),
	m_startupTime(0)
{}

void Transition::tryToFire()
{
	// cout << "Transition " << m_ID << " trying to fire" << endl;
	for (auto& p : m_inPlaces)
	{
		Place* const place = p.first;
		const int numTokens = p.second;

		assert(place->getCurrentMarking() >= numTokens);
		place->requestTokens(this, numTokens);
	}
}

void Transition::setLogFile(std::ofstream* file)
{
	m_log = file;
	m_bLoggingActive = true;
}