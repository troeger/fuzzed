#include "Probability.h"
#include "DecomposedFuzzyInterval.h"
#include "Interval.h"
#include "util.h"

namespace probability
{
	NumericInterval getAlphaCutBounds(const fuzztree::CrispProbability& prob)
	{
		const double val = prob.value();
		return NumericInterval(val, val);
	}


	NumericInterval getAlphaCutBounds(
		const DecomposedFuzzyInterval& alphaCuts,
		const double& alpha)
	{
		if (alphaCuts.find(alpha) != alphaCuts.end())
			return alphaCuts.at(alpha);

		// Alpha-cut needs to be approximated
		double lowerAlpha = 0.0;
		double upperAlpha = 1.0;

		// Search the biggest "lowerAlpha" and the lowest "upperAlpha"
		// such that lowerAlpha < alpha < upperAlpha 
		for (const auto& pair : alphaCuts)
		{
			const double a = pair.first;
			if (a < alpha && a > lowerAlpha)
				lowerAlpha = a;
			else if (a > alpha && a < upperAlpha)
				upperAlpha = a;
		}

		const NumericInterval lowerInterval = alphaCuts.at(lowerAlpha);
		const NumericInterval upperInterval = alphaCuts.at(upperAlpha);

		const double lowerBound = 
			lowerInterval.lowerBound + (alpha - lowerAlpha) * 
			(upperInterval.lowerBound- lowerInterval.lowerBound);

		const double upperBound = 
			upperInterval.upperBound + (upperAlpha - alpha) * 
			(lowerInterval.upperBound - upperInterval.upperBound);

		return NumericInterval(lowerBound, upperBound);
	}

	NumericInterval getAlphaCutBounds(const fuzztree::FailureRate& prob, const unsigned int& missionTime)
	{
		const double val = util::probabilityFromRate(prob.value(), missionTime);
		return NumericInterval(val, val);
	}

}