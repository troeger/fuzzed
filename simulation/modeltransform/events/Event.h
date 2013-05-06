#pragma once
#include "FaultTreeNode.h"

typedef float FuzzyNumber;

class Event : public FaultTreeNode
{
public:
	Event(const std::string& ID, long double failureRate, const std::string& name = "");
	Event(const std::string& ID, FuzzyNumber fuzzyFailureRate);
	
	virtual ~Event() {};

	virtual long double getValue() const override;

protected:
	long double m_failureRate;
};