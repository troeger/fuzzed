#pragma once
#include "Transition.h"
#include <boost/shared_ptr.hpp>

class ImmediateTransition : public Transition
{
public:
	typedef std::shared_ptr<ImmediateTransition> Ptr;

	ImmediateTransition(const std::string& id, double rate, int priority, double weight = 1.0, const std::string& label = "");

	// copying
	ImmediateTransition(const ImmediateTransition& other);
	ImmediateTransition& operator= (const ImmediateTransition &other);
	
	const int& getPriority() const { return m_priority; }
	const double& getWeight() const { return m_weight; }

protected:
	virtual bool stochasticallyEnabled(unsigned int tick) const override;

	double m_rate;

	double m_weight; // fires with probability P = weight/sumOfAllWeights
	int m_priority; // P1 > P2 -> 1 fires
};