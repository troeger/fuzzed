#pragma once
#include "Node.h"
#include "Dynamic2dArray.h"
#include <future>
#include <vector>

#include <fstream>

typedef std::vector<std::string> MinCut;
typedef std::vector<MinCut> MinCutAnalysisResult;
//typedef std::vector<std::vector<const fuzztree::Node*>> IntermediateMOCUSResult;
typedef Dynamic2dArray<const Node*> IntermediateMOCUSResult;

class MinCutAnalysisTask
{
public:
	MinCutAnalysisTask(const Node* const topEvent, std::ofstream& logfile);
	~MinCutAnalysisTask();

	MinCutAnalysisResult analyze();

protected:
	void analyzeRecursive(IntermediateMOCUSResult&, const Node&, unsigned int r, unsigned int c);

	static MinCutAnalysisResult minimizeResult(const IntermediateMOCUSResult&);
	
	const Node* const m_tree;

	std::ofstream& m_logFile;
};