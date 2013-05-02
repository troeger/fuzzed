#include "TimedTransition.h"
#include "implementation/Simulation.h"

TimedTransition::TimedTransition(const std::string& id, double rate)
	: Transition(id), 
	m_rate(rate), 
	m_r(-1), 
	m_wasNotEnabled(true)
{}

TimedTransition::TimedTransition(const TimedTransition& other)
	: Transition(other.m_ID), 
	m_rate(other.m_rate), 
	m_r(-1), 
	m_wasNotEnabled(true)
{}

bool TimedTransition::stochasticallyEnabled(int tick) const
{
	return m_r <= tick;
}

TimedTransition& TimedTransition::operator=(const TimedTransition &other)
{
	m_ID = other.m_ID;
	m_rate = other.m_rate;
	m_hasNotFired = true;
	m_r = -1;
	m_wasNotEnabled = true;
	return *this;
}

bool TimedTransition::tryUpdateStartupTime(int tick)
{
	if (m_hasNotFired && m_wasNotEnabled && enoughTokens())
	{
		m_wasNotEnabled = false;
		m_r += tick;
		return true;
	}
	return false;
}