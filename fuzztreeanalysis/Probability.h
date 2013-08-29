#pragma once
#include "Interval.h"
#include "faulttree.h"


namespace probability
{
	Interval getAlphaCutBounds(const faulttree::CrispProbability& prob);
//	Interval getAlphaCutBounds(const faulttree::DecomposedFuzzyProbability& prob);
	Interval getAlphaCutBounds(const faulttree::FailureRate& prob, const unsigned int& missionTime);

}