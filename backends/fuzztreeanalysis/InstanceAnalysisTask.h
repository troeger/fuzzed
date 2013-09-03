#pragma once
#include "fuzztree.h"
#include "DecomposedFuzzyInterval.h"
#include <map>

typedef DecomposedFuzzyInterval InstanceAnalysisResult;

/************************************************************************/
/* Analyzes one instance of a fuzztree.									*/
/* The fuzztree should ideally no longer contain variation points!		*/
/************************************************************************/

class InstanceAnalysisTask
{
public:
	InstanceAnalysisTask(fuzztree::TopEvent& tree, unsigned int decompositionNumber);
	InstanceAnalysisResult compute();
	
protected:
	fuzztree::TopEvent& m_tree;
	unsigned int m_decompositionNumber;
};