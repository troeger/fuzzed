#include "TimedTransition.h"
#include "implementation/Simulation.h"

TimedTransition::TimedTransition(const std::string& id, double rate, const std::string& label /*=""*/)
	: Transition(id, label), 
	m_rate(rate), 
	m_r(MAX_INT)
{}

TimedTransition::TimedTransition(const TimedTransition& other)
	: Transition(other.m_ID), 
	m_rate(other.m_rate), 
	m_r(MAX_INT)
{}

bool TimedTransition::stochasticallyEnabled(unsigned int tick) const
{
	return m_r <= tick; // TODO <= or <??
}

TimedTransition& TimedTransition::operator=(const TimedTransition &other)
{
	m_ID = other.m_ID;
	m_rate = other.m_rate;
	m_hasNotFired = true;
	m_r = MAX_INT;
	m_wasNotEnabled = true;
	return *this;
}

bool TimedTransition::tryUpdateStartupTime(const unsigned int& tick)
{
	if (m_hasNotFired && m_wasNotEnabled && enoughTokens())
	{
		m_wasNotEnabled = false;
		m_r += tick;
		return true;
	}
	return false;
}

void TimedTransition::setFiringTime(const unsigned int& t)
{
	m_r = t;
}
