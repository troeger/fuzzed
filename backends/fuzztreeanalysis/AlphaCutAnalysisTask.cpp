#include "AlphaCutAnalysisTask.h"
#include "Probability.h"
#include "NumericInterval.h"
#include "xmlutil.h"
#include "FatalException.h"

#include <math.h>
#include <algorithm>
#include <bitset>
#include <climits>
#include <exception>

using std::vector;
using std::string;

namespace
{
	static const std::string UNDEVELOPED_ERROR	= "The tree contains undeveloped events and cannot be analyzed.";
	static const std::string UNKNOWN_TYPE		= "Unknown child node type.";
}


AlphaCutAnalysisTask::AlphaCutAnalysisTask(const Node* topEvent, const unsigned int missionTime, const double alpha, std::ofstream& logfile)
: m_tree(topEvent), m_missionTime(missionTime), m_alpha(alpha), m_logFile(logfile), m_bDetectedUndeveloped(false)
{}

std::future<AlphaCutAnalysisResult> AlphaCutAnalysisTask::run()
{
	return std::async(std::launch::async, &AlphaCutAnalysisTask::analyze, this);
}

AlphaCutAnalysisResult AlphaCutAnalysisTask::analyze()
{
	if (m_tree->getChildren().size() == 0)
		return NumericInterval(1.0, 1.0); // trees without children are completely reliable
	return analyzeRecursive(m_tree->getChildren().front());
}

AlphaCutAnalysisResult AlphaCutAnalysisTask::analyzeRecursive(const Node& node)
{
	const std::string& typeName = node.getType();
	
	// Leaf nodes...
	if (typeName == nodetype::BASICEVENT) 
	{
		return node.getProbability().getAlphaCutBounds(m_missionTime);
	}
	else if (node.isEventSet())
	{
		// the Java code handled this, so the event sets were not expanded by the configuration
		// the C++ configuration code already expands event sets

		const string error = string("Unexpected Event Set (they should have been removed by configuration): ") + typeName;
		m_logFile << error << std::endl;
		
		throw FatalException(error, 0, node.getId());
	}
	else if (typeName == nodetype::HOUSEEVENT)
	{
		// TODO: new House Variation Point?
		return NumericInterval(1.0, 1.0);
	}
	else if (typeName == nodetype::UNDEVELOPEDEVENT)
	{
		m_logFile << "Found Undeveloped Event, ID: " << node.getId() << std::endl;
		if (m_bDetectedUndeveloped)
			return NumericInterval(); // this error was already reported once
		
		m_bDetectedUndeveloped = true;
		
		throw FatalException(UNDEVELOPED_ERROR, 0);
	}
	else if (typeName == nodetype::INTERMEDIATEEVENT)
	{
		if (node.getChildren().size() != 1)
		{
			m_logFile << "Intermediate Event size != 1, ID: , size: " << node.getId() << std::endl;
			if (node.getChildren().size() == 0)
				return NumericInterval(1.0, 1.0);
		}
		return analyzeRecursive(node.getChildren().front());
	}
	
	// Static Gates...
	else if (typeName == nodetype::AND)
	{
		interval_t lowerBound = 1.0;
		interval_t upperBound = 1.0;
		for (const auto& c : node.getChildren())
		{
			const auto res = analyzeRecursive(c);

			lowerBound *= res.lowerBound;
			upperBound *= res.upperBound;
		}
		return NumericInterval(lowerBound, upperBound);
	}
	else if (typeName == nodetype::OR)
	{
		interval_t lowerBound = 0.0;
		interval_t upperBound = 0.0;

		for (const auto& c : node.getChildren())
		{
			const auto res = analyzeRecursive(c);

			lowerBound += res.lowerBound - (lowerBound * res.lowerBound);
			upperBound += res.upperBound - (upperBound * res.upperBound);
		}

		return NumericInterval(lowerBound, upperBound);
	}
	else if (typeName == nodetype::XOR)
	{
		// Calculate results of children first.
		const unsigned int n = node.getChildren().size();

		vector<interval_t> lowerBounds;
		vector<interval_t> upperBounds;
		for (const auto& c : node.getChildren())
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
		const unsigned int numberOfCombinations = (int)std::pow(2, n);
		vector<interval_t> combinations(numberOfCombinations);
		for (unsigned int i = 0; i < numberOfCombinations; ++i)
		{
			vector<interval_t> perm;
			for (unsigned int j = 0; j < n; j++)
				perm.emplace_back((i >> j)&1 ? upperBounds[j] : lowerBounds[j]);

			combinations[i] = calculateExactlyOneOutOfN(perm, n);
		}

		return NumericInterval(
			*std::min_element(combinations.begin(), combinations.end()),
			*std::max_element(combinations.begin(), combinations.end()));
	}
	else if (typeName == nodetype::VOTINGOR)
	{
		const int k = node.getKOutOfN();
		const int n = node.getChildren().size();

		vector<interval_t> lowerBounds;
		vector<interval_t> upperBounds;

		for (const auto& c : node.getChildren())
		{
			const auto res = analyzeRecursive(c);
			lowerBounds.emplace_back(res.lowerBound);
			upperBounds.emplace_back(res.upperBound);
		}

		return NumericInterval(
			calculateKOutOfN(lowerBounds, k, n),
			calculateKOutOfN(upperBounds, k, n));
	}
	else
	{
		throw FatalException(UNKNOWN_TYPE);
	}


	return NumericInterval();
}

double AlphaCutAnalysisTask::calculateExactlyOneOutOfN(const vector<interval_t>& values, unsigned int n)
{
	interval_t result = 0.0;
	for (unsigned int i = 0; i < n; i++)
	{
		interval_t termResult = 1.0;
		for (unsigned int j = 0; j < n; j++)
		{
			// un-negate the ith value 
			termResult *= (i == j) ? (1 - values[j]) :  values[j];
		}
		result += termResult;
	}
	return result;
}

double AlphaCutAnalysisTask::calculateKOutOfN(const vector<interval_t>& values, unsigned int k, unsigned int n)
{
	assert(values.size() == n);
	
	vector<double> p;
	p.emplace_back(1.0);

	for (unsigned int i = 1; i <= k; i++)
		p.emplace_back(0.0);

	for (unsigned int i = 0; i < n; i++)
		for (unsigned int j = k; j >= 1; j--)
			p[j] = values[i] * p[j-1] + (1-values[i]) * p[j];

	return p[k];
}

AlphaCutAnalysisTask::~AlphaCutAnalysisTask()
{
	;
}