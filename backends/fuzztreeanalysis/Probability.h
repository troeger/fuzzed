#pragma once
#include "fuzztree.h"
#include "DecomposedFuzzyInterval.h"

namespace probability
{
	NumericInterval getAlphaCutBounds(const fuzztree::CrispProbability& prob);
	NumericInterval getAlphaCutBounds(const DecomposedFuzzyInterval& alphaCuts, const double& alpha);
	NumericInterval getAlphaCutBounds(const fuzztree::TriangularFuzzyInterval& interval, const double& alpha);
	NumericInterval getAlphaCutBounds(const fuzztree::FailureRate& prob, const unsigned int& missionTime);
}