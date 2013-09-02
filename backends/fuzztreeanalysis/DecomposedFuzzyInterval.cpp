#include "DecomposedFuzzyInterval.h"

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob)
{
	DecomposedFuzzyInterval res;

	for (const auto& alphaCut : prob.alphaCuts())
	{
		const auto alpha = alphaCut.key();
		const auto interval = alphaCut.value();

		res[alpha]  = NumericInterval(interval.lowerBound(), interval.upperBound());
	}
	return res;
}