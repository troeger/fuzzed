#pragma once
#include "fuzztree.h"
#include <future>
#include <vector>

#include <fstream>

typedef std::vector<std::string> MinCut;
typedef std::vector<MinCut> MinCutAnalysisResult;
typedef std::vector<std::vector<fuzztree::ChildNode*>> IntermediateMOCUSResult;

class MinCutAnalysisTask
{
public:
	MinCutAnalysisTask(const fuzztree::TopEvent* const topEvent, std::ofstream& logfile);
	~MinCutAnalysisTask();

	MinCutAnalysisResult analyze();

protected:
	void analyzeRecursive(IntermediateMOCUSResult&, const fuzztree::ChildNode&);

	static MinCutAnalysisResult minimizeResult(const IntermediateMOCUSResult&);

	const fuzztree::TopEvent* m_tree;

	std::ofstream& m_logFile;
};