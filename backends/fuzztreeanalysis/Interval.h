#pragma once

struct Interval
{
	Interval() : lowerBound(0.0), upperBound(0.0) {}

	Interval(const double& lower, const double& upper):
		lowerBound(lower), upperBound(upper) {}

	double lowerBound;
	double upperBound;
};