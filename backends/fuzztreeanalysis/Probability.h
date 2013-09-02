#pragma once
#include "faulttree.h"
#include "DecomposedFuzzyInterval.h"

namespace probability
{
	Interval getAlphaCutBounds(const faulttree::CrispProbability& prob);
	Interval getAlphaCutBounds(const DecomposedFuzzyInterval& alphaCuts, const double& alpha);
	Interval getAlphaCutBounds(const faulttree::FailureRate& prob, const unsigned int& missionTime);
}