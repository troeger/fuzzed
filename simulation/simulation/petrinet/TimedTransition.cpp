#include "TimedTransition.h"
#include "implementation/Simulation.h"

TimedTransition::TimedTransition(const std::string& id, double rate, int r)
	: Transition(id), m_rate(rate), m_r(r)
{}

TimedTransition::TimedTransition(const TimedTransition& other)
	: Transition(other.m_ID), m_rate(other.m_rate), m_r(other.m_r)
{
	m_startupTime = 0;
}

bool TimedTransition::stochasticallyEnabled(int tick) const
{
	return (m_r + m_startupTime) <= tick;
}

TimedTransition& TimedTransition::operator=(const TimedTransition &other)
{
	m_ID = other.m_ID;
	m_rate = other.m_rate;
	m_active = true;
	m_bLoggingActive = other.m_bLoggingActive;
	m_r = other.m_r;
	m_startupTime = other.m_startupTime;
	m_startupTime = 0;
	return *this;
}