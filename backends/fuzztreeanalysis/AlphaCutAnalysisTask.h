#pragma once
#include "Interval.h"
#include "faulttree.h"
#include <future>

typedef Interval AlphaCutAnalysisResult;

class AlphaCutAnalysisTask
{
public:
	AlphaCutAnalysisTask(const faulttree::TopEvent* topEvent, const double& alpha);

	void run();

	std::future<AlphaCutAnalysisResult>* getFuture() { return &m_future; }
	const double& getAlpha() const { return m_alpha; }

protected:
	AlphaCutAnalysisResult analyze();
	AlphaCutAnalysisResult analyzeRecursive(const faulttree::ChildNode&);

	const double m_alpha;
	const faulttree::TopEvent* m_tree;

	std::future<AlphaCutAnalysisResult> m_future;
};