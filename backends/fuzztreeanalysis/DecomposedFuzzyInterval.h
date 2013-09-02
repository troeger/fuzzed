#pragma once
#include "fuzztree.h"
#include "Interval.h"

typedef std::map<double, Interval> DecomposedFuzzyInterval;

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob); // TODO