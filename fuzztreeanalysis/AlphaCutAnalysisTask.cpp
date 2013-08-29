#include "AlphaCutAnalysisTask.h"
#include "faulttree.h"
#include "FaultTreeTypes.h"
#include "Probability.h"
#include "Interval.h"

using namespace faulttree;

AlphaCutAnalysisTask::AlphaCutAnalysisTask(const faulttree::TopEvent* topEvent, const double& alpha)
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
	using namespace faultTreeType;

	const type_info& typeName = typeid(node);
	bool alreadyAdded = false;

	// Leaf nodes...
	if (typeName == *BASICEVENT) 
	{
		const auto& prob = (static_cast<const faulttree::BasicEvent&>(node)).probability();
		const type_info& probType = typeid(prob);

		double failureRate = 0.f;
		if (probType == *CRISPPROB)
		{
			return probability::getAlphaCutBounds(static_cast<const faulttree::CrispProbability&>(prob));
		}
		else if (probType == *FUZZYPROB)
		{
			// 				return probability::getAlphaCutBounds(
			// 					static_cast<const faulttree::DecomposedFuzzyProbability&>(prob),
			// 					m_tree->missionTime(), 
			// 					m_alpha);
		}
		else if (probType == *FAILURERATE)
		{
			return probability::getAlphaCutBounds(static_cast<const faulttree::FailureRate&>(prob), m_tree->missionTime());
		}
	}
	else if (typeName == *HOUSEEVENT)
	{
		return Interval(1.0, 1.0);
	}
	else if (typeName == *UNDEVELOPEDEVENT)
	{
		throw std::runtime_error("Cannot analyze trees with undeveloped events!");
		return Interval();
	}
	else if (typeName == *INTERMEDIATEEVENT)
	{

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
		return Interval(lowerBound, upperBound);
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

		return Interval(lowerBound, upperBound);
	}
	else if (typeName == *XOR)
	{

	}
	else if (typeName == *VOTINGOR)
	{

	}
}
