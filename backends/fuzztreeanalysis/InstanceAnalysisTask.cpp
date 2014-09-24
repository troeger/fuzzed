#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "Probability.h"

#include <assert.h>
#include <map>
#include <future>
#include <iostream>

using std::map;
using std::future;

InstanceAnalysisTask::InstanceAnalysisTask(const Node* tree, unsigned int decompositionNumber, unsigned int missionTime, std::ofstream& logfile) :
	m_tree(tree),
	m_decompositionNumber(decompositionNumber),
	m_missionTime(missionTime),
	m_logFile(logfile)
{}

InstanceAnalysisResult InstanceAnalysisTask::compute()
{
	return isFuzzy(m_tree) ? computeDecomposedResult() : computeSingleResult();
}

DecomposedFuzzyInterval InstanceAnalysisTask::computeDecomposedResult()
{
	map<AlphaCutAnalysisTask*, future<AlphaCutAnalysisResult>> alphaCutResults;
	DecomposedFuzzyInterval resultInterval;
	
	// TODO: some more intelligent way of dividing work.
	// find out whether this performs better than the serial version anyway.

	// TODO: reason about multi-threaded logging...

	// FORK
	for (unsigned int i = 0; i <= m_decompositionNumber; ++i)
	{
		const double alpha = (double)(i / m_decompositionNumber);
		AlphaCutAnalysisTask* task = new AlphaCutAnalysisTask(m_tree, m_missionTime, alpha, m_logFile);
		alphaCutResults[task] = task->run();
	}

	// JOIN
	for (auto& t : alphaCutResults)
	{
		const auto task		= t.first;
		const auto alphaCut = t.second.get(); // blocks until result is ready

		resultInterval[task->getAlpha()] = alphaCut;

		delete task;
	}
	return resultInterval;
}

const bool InstanceAnalysisTask::isFuzzy(const Node* node)
{
	bool fuzzy = false;

	if (node->getType() == nodetype::BASICEVENT) 
	{
		return node->getProbability().isFuzzy();
	}

	for (const auto& child : node->getChildren())
	{
		fuzzy |= isFuzzy(&child);
	}
	return fuzzy;
}

DecomposedFuzzyInterval InstanceAnalysisTask::computeSingleResult()
{
	future<AlphaCutAnalysisResult> alphaCutResult;
	DecomposedFuzzyInterval resultInterval;

	AlphaCutAnalysisTask* task = new AlphaCutAnalysisTask(m_tree, m_missionTime, 0.0, m_logFile);
	alphaCutResult = task->run();

	resultInterval[task->getAlpha()] = alphaCutResult.get();
	return resultInterval;
}

