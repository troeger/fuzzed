#pragma once
#include "Node.h"
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
		const Node* tree,
		unsigned int decompositionNumber,
		unsigned int missionTime,
		std::ofstream& logfile);

	InstanceAnalysisResult compute();
	
protected:
	DecomposedFuzzyInterval computeDecomposedResult();
	DecomposedFuzzyInterval computeSingleResult();

	static const bool isFuzzy(const Node* tree);

	const Node* m_tree;
	unsigned int m_decompositionNumber;
	unsigned int m_missionTime;

	std::ofstream& m_logFile;
};