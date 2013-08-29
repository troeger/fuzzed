#pragma once
#include "faulttree.h"
typedef double InstanceAnalysisResult; // TODO find out how this is structured

class InstanceAnalysisTask
{
public:
	InstanceAnalysisTask(faulttree::TopEvent& tree, unsigned int decompositionNumber);

	void compute();
	
protected:
	faulttree::TopEvent& m_tree;
	unsigned int m_decompositionNumber;
};