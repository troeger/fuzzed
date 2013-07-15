#pragma once
#include "FaultTreeNode.h"

typedef float FuzzyNumber;

class Event : public FaultTreeNode
{
public:
	Event(const std::string& ID, long double failureRate, const std::string& name = "");
	Event(const std::string& ID, FuzzyNumber fuzzyFailureRate);
	
	virtual ~Event() {};

	virtual int serializeTimeNet(boost::shared_ptr<TNDocument> doc) const override;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const override;

	const long double& getFailureRate() const { return m_failureRate; }

protected:
	long double m_failureRate;
};