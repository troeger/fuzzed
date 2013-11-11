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
	InstanceAnalysisTask(
		fuzztree::TopEvent* tree,
		unsigned int decompositionNumber,
		std::ofstream& logfile);

	InstanceAnalysisResult compute();
	
	// static void serializeResult(const InstanceAnalysisResult& res, pugi::xml_document doc);

protected:
	fuzztree::TopEvent* m_tree;
	unsigned int m_decompositionNumber;

	std::ofstream& m_logFile;
};