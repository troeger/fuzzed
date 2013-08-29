#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"

#include <assert.h>
#include <vector>
#include <future>

using std::vector;
using std::future;

InstanceAnalysisTask::InstanceAnalysisTask(faulttree::TopEvent& tree, unsigned int decompositionNumber) :
	m_tree(tree),
	m_decompositionNumber(decompositionNumber)
{}

InstanceAnalysisResult InstanceAnalysisTask::compute()
{
	vector<AlphaCutAnalysisTask*> alphaCutTasks;
	const double m = (double)m_decompositionNumber;
	
	// FORK
	for (unsigned int i = 0; i <= m_decompositionNumber; ++i)
	{
		const double alpha = i / m;
		AlphaCutAnalysisTask* subTask = new AlphaCutAnalysisTask(&m_tree, alpha);
		subTask->run();
		alphaCutTasks.emplace_back(subTask);
	}

	// JOIN
	DecomposedFuzzyInterval result;
	for (auto& t : alphaCutTasks)
	{
		result[t->getAlpha()] = t->getFuture()->get();
		delete t;
	}

	return result;
}

