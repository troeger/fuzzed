#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"

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
	map<double, future<AlphaCutAnalysisResult>> alphaCutResults;
	const double m = (double)m_decompositionNumber;
	
	// FORK
	for (unsigned int i = 1; i <= m_decompositionNumber; ++i)
	{
		const double alpha = i / m;
		AlphaCutAnalysisTask task(m_tree, alpha);
		alphaCutResults[alpha] = task.run();
	}

	// JOIN
	DecomposedFuzzyInterval result;
	for (auto& t : alphaCutResults)
	{
		result[t.first] = t.second.get();
	}

	return result;
}

