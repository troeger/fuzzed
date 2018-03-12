#include "ImmediateTransition.h"

bool ImmediateTransition::stochasticallyEnabled(unsigned int) const 
{
	return true;
}

ImmediateTransition::ImmediateTransition(const std::string& id, double rate, int priority, double weight, const std::string& label /*= ""*/)
	: Transition(id, label), 
	m_rate(rate), 
	m_weight(weight),
	m_priority(priority)
{}

ImmediateTransition::ImmediateTransition(const ImmediateTransition& other)
	: Transition(other.m_ID, other.m_label), 
	m_rate(other.m_rate), 
	m_weight(other.m_weight),
	m_priority(other.m_priority)
{}

ImmediateTransition& ImmediateTransition::operator=(const ImmediateTransition &other)
{
	m_ID = other.m_ID;
	m_label = other.m_label;
	
	m_rate = other.m_rate;
	m_priority = other.m_priority;
	m_weight = other.m_weight;

	return *this;
}
