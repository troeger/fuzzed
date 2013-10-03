#pragma once
#include "Transition.h"
#include <set>
#include <boost/shared_ptr.hpp>

class TimedTransition : public Transition
{
public:
	typedef std::shared_ptr<TimedTransition> Ptr;

	TimedTransition(const std::string& ID, double rate, const std::string& label = "");

	// copying
	TimedTransition(const TimedTransition& other);
	TimedTransition& operator= (const TimedTransition &other);

	double getRate() const { return m_rate; }
	unsigned int getFiringTime() const { return m_r; }

	// TODO: find out if float would increase precision
	void setFiringTime(const unsigned int& t);
	bool tryUpdateStartupTime(const unsigned int& tick);

protected:
	virtual bool stochasticallyEnabled(unsigned int tick) const override;

	double m_rate;

	unsigned int m_r;
};