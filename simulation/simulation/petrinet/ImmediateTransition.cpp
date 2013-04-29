#include "ImmediateTransition.h"

bool ImmediateTransition::stochasticallyEnabled(int tick) const 
{
	return true;
}

ImmediateTransition::ImmediateTransition(const std::string& id, double rate, double priority)
	: Transition(id), m_rate(rate), m_priority(priority)
{}

ImmediateTransition& ImmediateTransition::operator=(const ImmediateTransition &other)
{
	m_ID = other.m_ID;
	m_rate = other.m_rate;
	m_active = true;
	m_bLoggingActive = other.m_bLoggingActive;

	return *this;
}

ImmediateTransition::ImmediateTransition(const ImmediateTransition& other)
	: Transition(other.m_ID), m_rate(other.m_rate), m_priority(other.m_priority)
{}