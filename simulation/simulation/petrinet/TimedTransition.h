#pragma once
#include "Transition.h"
#include <set>
#include <boost/shared_ptr.hpp>

class TimedTransition : public Transition
{
public:
	typedef boost::shared_ptr<TimedTransition> Ptr;

	TimedTransition(const std::string& id, double rate, int r);

	// copying
	TimedTransition(const TimedTransition& other);
	TimedTransition& operator= (const TimedTransition &other);

	// TODO floats sufficient here?
	double getRate() const { return m_rate; };
	int getFiringTime() const { return m_r; };
	void setFiringTime(int t) { m_r = t; };

protected:
	virtual bool stochasticallyEnabled(int tick) override;

	double m_rate;
	int m_r;
};