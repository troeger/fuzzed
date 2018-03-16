#pragma once
#include "fuzztree.h"
#include "common.h"
#include "Interval.h"

// TODO: this should become obsolete once the commonTypes are really shared

typedef std::map<double, NumericInterval> DecomposedFuzzyInterval;

DecomposedFuzzyInterval parse(const fuzztree::DecomposedFuzzyProbability& prob);
commonTypes::DecomposedFuzzyProbability serialize(const DecomposedFuzzyInterval& interval);
