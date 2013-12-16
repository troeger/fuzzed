#pragma once
#include "FaultTreeNode.h"
#include <cassert>

typedef float FuzzyNumber;

class Event : public FaultTreeNode
{
public:
	Event(const std::string& ID, double failureRate, const std::string& name = "");
	Event(const std::string& ID, FuzzyNumber fuzzyFailureRate);
	
	virtual std::string serializeAsFormula(std::shared_ptr<PNDocument> doc) const override;

	const double& getFailureRate() const { return m_failureRate; }

protected:
	double m_failureRate;
};