#pragma once

struct NumericInterval
{
	NumericInterval() : lowerBound(0.0), upperBound(0.0) {};

	NumericInterval(const double& lower, const double& upper):
		lowerBound(lower), upperBound(upper) {};

	double lowerBound;
	double upperBound;
};