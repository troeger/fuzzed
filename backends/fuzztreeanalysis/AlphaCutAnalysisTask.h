#pragma once
#include "Interval.h"
#include "fuzztree.h"
#include <future>
#include <vector>
#pragma strict_gs_check(on)

typedef NumericInterval AlphaCutAnalysisResult;

class AlphaCutAnalysisTask
{
public:
	AlphaCutAnalysisTask(const fuzztree::TopEvent* topEvent, const double alpha);
	~AlphaCutAnalysisTask();

	std::future<AlphaCutAnalysisResult> run();

	const double& getAlpha() const { return m_alpha; }

protected:
	static double calculateExactlyOneOutOfN(const std::vector<double>& values, unsigned int n);
	static double calculateKOutOfN(const std::vector<double>& values, unsigned int k, unsigned int n);


	AlphaCutAnalysisResult analyze();
	AlphaCutAnalysisResult analyzeRecursive(const fuzztree::ChildNode&);

	const double m_alpha;
	const fuzztree::TopEvent* m_tree;
};