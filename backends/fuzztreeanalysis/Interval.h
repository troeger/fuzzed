#pragma once

typedef double interval_t;

struct NumericInterval
{
	NumericInterval() : lowerBound(0.0), upperBound(0.0) {};

	NumericInterval(const interval_t& lower, const interval_t& upper):
		lowerBound(lower), upperBound(upper) {};

	interval_t lowerBound;
	interval_t upperBound;
};