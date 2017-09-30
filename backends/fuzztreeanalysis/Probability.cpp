#include "Probability.h"
#include "DecomposedFuzzyInterval.h"
#include "Interval.h"
#include "util.h"

namespace probability
{
	NumericInterval getAlphaCutBounds(const fuzztree::CrispProbability& prob)
	{
		const interval_t val = static_cast<interval_t>(prob.value());
		return NumericInterval(val, val);
	}


	NumericInterval getAlphaCutBounds(
		const DecomposedFuzzyInterval& alphaCuts,
		const double& alpha)
	{
		if (alphaCuts.find(alpha) != alphaCuts.end())
			return alphaCuts.at(alpha);

		// Alpha-cut needs to be approximated
		interval_t lowerAlpha = 0.0;
		interval_t upperAlpha = 1.0;

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

		const interval_t lowerBound = 
			lowerInterval.lowerBound + (alpha - lowerAlpha) * 
			(upperInterval.lowerBound- lowerInterval.lowerBound);

		const interval_t upperBound = 
			upperInterval.upperBound + (upperAlpha - alpha) * 
			(lowerInterval.upperBound - upperInterval.upperBound);

		return NumericInterval(lowerBound, upperBound);
	}

	NumericInterval getAlphaCutBounds(const fuzztree::FailureRate& prob, const unsigned int& missionTime)
	{
		const interval_t val = util::probabilityFromRate(prob.value(), missionTime);
		return NumericInterval(val, val);
	}

	NumericInterval getAlphaCutBounds(const fuzztree::TriangularFuzzyInterval& interval, const double& alpha)
	{
		const auto a = interval.a();
		const auto c = interval.c();
		
		const interval_t lowerBound = alpha * (interval.b1() - a) + a;
		const interval_t upperBound = c - alpha * (c - interval.b2());

		return NumericInterval(lowerBound, upperBound);
	}
}
