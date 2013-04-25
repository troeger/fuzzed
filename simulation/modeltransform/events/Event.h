#pragma once
#include "FaultTreeNode.h"

typedef float FuzzyNumber;

class Event : public FaultTreeNode
{
public:
	Event(int ID, long double failureRate, const std::string& name = "");
	Event(int ID, FuzzyNumber fuzzyFailureRate);
	
	virtual ~Event() {};

	virtual long double getValue() const override;

protected:
	long double m_failureRate;
};