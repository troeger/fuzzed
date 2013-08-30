#pragma once
#include "Interval.h"
#include "faulttree.h"

class DecomposedFuzzyInterval;

namespace probability
{
	Interval getAlphaCutBounds(const faulttree::CrispProbability& prob);
	Interval getAlphaCutBounds(const DecomposedFuzzyInterval& alphaCuts, const double& alpha);
	Interval getAlphaCutBounds(const faulttree::FailureRate& prob, const unsigned int& missionTime);

}