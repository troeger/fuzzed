#include "AlphaCutAnalysisTask.h"
#include "FuzzTreeTypes.h"
#include "Probability.h"
#include "Interval.h"

#include <math.h>
#include <algorithm>
#include <bitset>
#include <climits>

using namespace fuzztree;
using std::vector;

AlphaCutAnalysisTask::AlphaCutAnalysisTask(const TopEvent* topEvent, const double& alpha)
	: m_tree(topEvent),
	m_alpha(alpha)
{}

void AlphaCutAnalysisTask::run()
{
	m_future = std::async(&AlphaCutAnalysisTask::analyze, this);
}

AlphaCutAnalysisResult AlphaCutAnalysisTask::analyze()
{
	return analyzeRecursive(m_tree->children().front());
}

AlphaCutAnalysisResult AlphaCutAnalysisTask::analyzeRecursive(const ChildNode& node)
{
	using namespace fuzztreeType;

	const type_info& typeName = typeid(node);
	
	// Leaf nodes...
	if (typeName == *BASICEVENT) 
	{
		const auto& prob = (static_cast<const fuzztree::BasicEvent&>(node)).probability();
		const type_info& probType = typeid(prob);

		if (probType == *CRISPPROB)
		{
			return probability::getAlphaCutBounds(static_cast<const fuzztree::CrispProbability&>(prob));
		}
		else if (probType == *FUZZYPROB)
		{
			return probability::getAlphaCutBounds(parse(static_cast<const fuzztree::DecomposedFuzzyProbability&>(prob)), m_alpha);
		}
		else if (probType == *FAILURERATE)
		{
			return probability::getAlphaCutBounds(static_cast<const fuzztree::FailureRate&>(prob), m_tree->missionTime());
		}
	}
	else if (typeName == *BASICEVENTSET || typeName == *INTERMEDIATEEVENTSET)
	{
		// the java code handled this, so the event sets were not expanded by the configuration
		// the C++ configuration code already expands event sets
		assert(false);
	}
	else if (typeName == *HOUSEEVENT)
	{
		return NumericInterval(1.0, 1.0);
	}
	else if (typeName == *UNDEVELOPEDEVENT)
	{
		throw std::runtime_error("Cannot analyze trees with undeveloped events!");
		return NumericInterval();
	}
	else if (typeName == *INTERMEDIATEEVENT)
	{
		assert(node.children().size() == 1);
		return analyzeRecursive(node.children().front());
	}

	// Static Gates...
	else if (typeName == *AND)
	{
		double lowerBound = 1.0;
		double upperBound = 1.0;
		for (const auto& c : node.children())
		{
			const auto res = analyzeRecursive(c);

			lowerBound *= res.lowerBound;
			upperBound *= res.upperBound;
		}
		return NumericInterval(lowerBound, upperBound);
	}
	else if (typeName == *OR)
	{
		double lowerBound = 0.0;
		double upperBound = 0.0;

		for (const auto& c : node.children())
		{
			const auto res = analyzeRecursive(c);

			lowerBound += res.lowerBound - (lowerBound * res.lowerBound);
			upperBound += res.upperBound - (upperBound * res.upperBound);
		}

		return NumericInterval(lowerBound, upperBound);
	}
	else if (typeName == *XOR)
	{
		// Calculate results of children first.
		const unsigned int n = node.children().size();

		vector<double> lowerBounds(n);
		vector<double> upperBounds(n);
		for (const auto& c : node.children())
		{
			const auto res = analyzeRecursive(c);
			/*
			 * ATTENTION: Here the values are negated since this is more efficient
			 * (there are much more negated terms than not-negated).
			 */
			lowerBounds.emplace_back(1 - res.lowerBound);
			upperBounds.emplace_back(1 - res.upperBound);
		}

		// Get all permutations of lower and upper bounds (idea see VotingOr gate).
		const unsigned int numberOfCombinations = (int) std::pow(2, n);
		vector<double> combinations(numberOfCombinations);
		for (unsigned int i = 0; i < numberOfCombinations; ++i)
		{
			const std::bitset<UINT_MAX> choice(i);
			vector<double> perm(n);
			for (unsigned int j = 0; j < n; j++)
				perm.emplace_back(choice[j] ? upperBounds[j] : lowerBounds[j]);

			combinations[i] = calculateExactlyOneOutOfN(perm, n);
		}

		return NumericInterval(
			*std::min_element(combinations.begin(), combinations.end()),
			*std::max_element(combinations.begin(), combinations.end()));
	}
	else if (typeName == *VOTINGOR)
	{
		const auto votingOr = static_cast<const fuzztree::VotingOr&>(node);
		
		const int k = votingOr.k();
		const int n = votingOr.children().size();

		vector<double> lowerBounds(n);
		vector<double> upperBounds(n);

		int i = 0;
		for (const auto& c : node.children())
		{
			const auto res = analyzeRecursive(c);
			lowerBounds.emplace_back(res.lowerBound);
			upperBounds.emplace_back(res.upperBound);
		}

		return NumericInterval(calculateKOutOfN(lowerBounds, k, n), calculateKOutOfN(upperBounds, k, n));
	}
}

double AlphaCutAnalysisTask::calculateExactlyOneOutOfN(const vector<double>& values, unsigned int n)
{
	double result = 0.0;
	for (unsigned int i = 0; i < n; i++)
	{
		double termResult = 1.0;
		for (unsigned int j = 0; j < n; j++)
		{
			// un-negate the ith value 
			termResult *= (i == j) ? (1 - values[j]) :  values[j];
		}
		result += termResult;
	}
	return result;
}

double AlphaCutAnalysisTask::calculateKOutOfN(const vector<double>& values, unsigned int k, unsigned int n)
{
	assert(values.size() == n);
	
	vector<double> p(k+1);
	p.emplace_back(1.0);

	for (unsigned int i = 1; i <= k; i++)
		p.emplace_back(0.0);

	for (unsigned int i = 0; i < n; i++)
		for (unsigned int j = k; j >= 1; j--)
			p[j] = values[i] * p[j-1] + (1-values[i]) * p[j];

	return p[k];
}
