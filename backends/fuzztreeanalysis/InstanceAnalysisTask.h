#pragma once
#include "fuzztree.h"
#include "DecomposedFuzzyInterval.h"
#include <map>

typedef DecomposedFuzzyInterval InstanceAnalysisResult;

class InstanceAnalysisTask
{
public:
	InstanceAnalysisTask(fuzztree::TopEvent& tree, unsigned int decompositionNumber);
	InstanceAnalysisResult compute();
	
protected:
	fuzztree::TopEvent& m_tree;
	unsigned int m_decompositionNumber;
};