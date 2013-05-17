#include "ImmediateTransition.h"

bool ImmediateTransition::stochasticallyEnabled(unsigned int tick) const 
{
	return true;
}

ImmediateTransition::ImmediateTransition(const std::string& id, double rate, double priority, const std::string& label /*= ""*/)
	: Transition(id, label), m_rate(rate), m_priority(priority)
{}

ImmediateTransition& ImmediateTransition::operator=(const ImmediateTransition &other)
{
	m_ID = other.m_ID;
	m_rate = other.m_rate;
	m_hasNotFired = true;
	m_priority = other.m_priority;

	return *this;
}

ImmediateTransition::ImmediateTransition(const ImmediateTransition& other)
	: Transition(other.m_ID), m_rate(other.m_rate), m_priority(other.m_priority)
{}