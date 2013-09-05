#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "Probability.h"

#include <assert.h>
#include <map>
#include <future>

using std::map;
using std::future;

InstanceAnalysisTask::InstanceAnalysisTask(fuzztree::TopEvent* tree, unsigned int decompositionNumber) :
	m_tree(tree),
	m_decompositionNumber(decompositionNumber)
{}

InstanceAnalysisResult InstanceAnalysisTask::compute()
{
	map<AlphaCutAnalysisTask*, future<AlphaCutAnalysisResult>> alphaCutResults;
	DecomposedFuzzyInterval resultInterval;

	const double m = (double)m_decompositionNumber;
	
	// FORK
	for (unsigned int i = 0; i <= m_decompositionNumber; ++i)
	{
		const double alpha = (double)(i / m);
		AlphaCutAnalysisTask* task = new AlphaCutAnalysisTask(m_tree, alpha);
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

