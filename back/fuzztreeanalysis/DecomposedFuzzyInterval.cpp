#include "DecomposedFuzzyInterval.h"

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob)
{
	DecomposedFuzzyInterval res;

	for (const auto& alphaCut : prob.alphaCuts())
	{
		const auto alpha	= alphaCut.key();
		const auto interval	= alphaCut.value();

		res[alpha] = NumericInterval(interval.lowerBound(), interval.upperBound());
	}
	return res;
}

commonTypes::DecomposedFuzzyProbability serialize(const DecomposedFuzzyInterval& interval)
{
	commonTypes::DecomposedFuzzyProbability res;

	for (const auto& alphaCut : interval)
	{
		const double alpha = alphaCut.first;
		const NumericInterval& numInterval = alphaCut.second; 
		
		res.alphaCuts().push_back(commonTypes::DoubleToIntervalMap(
			commonTypes::Interval(numInterval.lowerBound, numInterval.upperBound), alpha));
	}
	return res;
}
