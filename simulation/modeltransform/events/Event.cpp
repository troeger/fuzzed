#include "Event.h"

Event::Event(int ID, long double failureRate, const std::string& name/* = ""*/)
	: FaultTreeNode(ID, name), m_failureRate(failureRate)
{
}


// big fat TODO
Event::Event(int ID, FuzzyNumber fuzzyFailureRate)
	: FaultTreeNode(ID), m_failureRate(fuzzyFailureRate)
{
}

long double Event::getValue() const 
{
	return m_failureRate;
}