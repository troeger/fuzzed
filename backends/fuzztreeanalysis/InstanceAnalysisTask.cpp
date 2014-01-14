#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "Probability.h"
#include "FuzzTreeTypes.h"

#include <assert.h>
#include <map>
#include <future>


using std::map;
using std::future;

InstanceAnalysisTask::InstanceAnalysisTask(const fuzztree::TopEvent* tree, unsigned int decompositionNumber, std::ofstream& logfile) :
	m_tree(tree),
	m_decompositionNumber(decompositionNumber),
	m_logFile(logfile)
{}

InstanceAnalysisResult InstanceAnalysisTask::compute()
{
	return isFuzzy(m_tree) ? computeDecomposedResult() : computeSingleResult();
}

InstanceAnalysisResult InstanceAnalysisTask::computeDecomposedResult()
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
		AlphaCutAnalysisTask* task = new AlphaCutAnalysisTask(m_tree, alpha, m_logFile);
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

const bool InstanceAnalysisTask::isFuzzy(const fuzztree::Node* node)
{
	bool fuzzy = false;

	using namespace fuzztreeType;
	const type_info& typeName = typeid(*node);

	if (typeName == *BASICEVENT) 
	{
		const type_info& probName = typeid((static_cast<const fuzztree::BasicEvent*>(node))->probability());
		return (probName == *TRIANGULARFUZZYINTERVAL || probName == *DECOMPOSEDFUZZYINTERVAL);
	}

	for (const auto& child : node->children())
	{
		fuzzy &= isFuzzy(&child);
	}
	return fuzzy;
}

InstanceAnalysisResult InstanceAnalysisTask::computeSingleResult()
{
	future<AlphaCutAnalysisResult> alphaCutResult;
	DecomposedFuzzyInterval resultInterval;

	AlphaCutAnalysisTask* task = new AlphaCutAnalysisTask(m_tree, 1, m_logFile);
	alphaCutResult = task->run();

	resultInterval[task->getAlpha()] = alphaCutResult.get();
	return resultInterval;
}

