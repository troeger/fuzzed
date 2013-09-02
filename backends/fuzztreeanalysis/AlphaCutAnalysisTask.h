#pragma once
#include "Interval.h"
#include "fuzztree.h"
#include <future>

typedef NumericInterval AlphaCutAnalysisResult;

class AlphaCutAnalysisTask
{
public:
	AlphaCutAnalysisTask(const fuzztree::TopEvent* topEvent, const double& alpha);

	void run();

	std::future<AlphaCutAnalysisResult>* getFuture() { return &m_future; }
	const double& getAlpha() const { return m_alpha; }

protected:
	AlphaCutAnalysisResult analyze();
	AlphaCutAnalysisResult analyzeRecursive(const fuzztree::ChildNode&);

	const double m_alpha;
	const fuzztree::TopEvent* m_tree;

	std::future<AlphaCutAnalysisResult> m_future;
};