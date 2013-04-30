#include "Transition.h"
#include <typeinfo>
#include "Place.h"
#include "util.h"

void Transition::fire(int tick)
{
	// cout << "Firing: " << m_ID << endl;
	m_hasNotFired = false;

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
	return 
		m_hasNotFired &&
		enoughTokens() &&
		stochasticallyEnabled(tick);
}

Transition::Transition(const string& id)
	: m_ID(id),
	m_bLoggingActive(false),
	m_hasNotFired(true),
	m_log(nullptr)
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

bool Transition::enoughTokens() const
{
	for (const auto& p : m_inPlaces)
	{
		const int currentMarking = p.first->getCurrentMarking();
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

Transition::~Transition()
{
	if (m_log)
		delete m_log;
}
