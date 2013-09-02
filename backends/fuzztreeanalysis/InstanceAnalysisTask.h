#pragma once
#include "faulttree.h"
#include "DecomposedFuzzyInterval.h"
#include <map>

typedef DecomposedFuzzyInterval InstanceAnalysisResult;

class InstanceAnalysisTask
{
public:
	InstanceAnalysisTask(faulttree::TopEvent& tree, unsigned int decompositionNumber);
	InstanceAnalysisResult compute();
	
protected:
	faulttree::TopEvent& m_tree;
	unsigned int m_decompositionNumber;
};