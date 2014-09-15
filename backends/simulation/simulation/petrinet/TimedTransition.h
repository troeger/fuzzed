#pragma once
#include "Transition.h"
#include <set>
#include <boost/shared_ptr.hpp>

/**
 * Class: TimedTransition
 * A transition which fires after an exponentially distributed delay, after enabling.
 * Firing policy: race with enabling memory
 */
class TimedTransition : public Transition
{
public:
	typedef std::shared_ptr<TimedTransition> Ptr;

	/**
	 * Constructor: TimedTransition
	 * 
	 * Parameters:
	 *	ID - the unique transition identifier.
	 *	rate - the rate parameter for the underlying exponential distribution.
	 *	label - an optional description string for the transition.
	 */
	TimedTransition(const std::string& ID, double rate, const std::string& label = "");

	// copying
	TimedTransition(const TimedTransition& other);
	TimedTransition& operator= (const TimedTransition &other);

	double getRate() const { return m_rate; }
	unsigned int getFiringTime() const { return m_r; }

	/**
	 * Function: setFiringTime
	 * Sets the (exponentially distributed) firing time to a future t.
	 */
	void setFiringTime(const unsigned int& t);

	/**
	 * Function: tryUpdateStartupTime
	 * If the transition (which corresponds to an error event in the fault tree) has not yet fired and is enabled, delay its firing by d.
	 */
	bool tryUpdateStartupTime(const unsigned int& d);

protected:
	virtual bool stochasticallyEnabled(unsigned int tick) const override;

	double m_rate;

	unsigned int m_r;
};