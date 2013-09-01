#pragma once
#include "Interval.h"
#include "fuzztree.h"

typedef std::map<double, Interval> DecomposedFuzzyInterval;

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob) { return DecomposedFuzzyInterval(); } // TODO