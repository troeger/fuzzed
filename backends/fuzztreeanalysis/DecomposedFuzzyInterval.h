#pragma once
#include "Interval.h"

typedef std::map<double, Interval> DecomposedFuzzyInterval;

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob) { return DecomposedFuzzyInterval(); } // TODO