#include "AlphaCutAnalysisTask.h"
#include "FuzzTreeTypes.h"
#include "Probability.h"
#include "Interval.h"

using namespace fuzztree;

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

	}
	else if (typeName == *VOTINGOR)
	{

	}
}
