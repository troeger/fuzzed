#pragma once
#include "fuzztree.h"
#include "MinCut.h"
#include <future>
#include <vector>

#include <fstream>

typedef std::vector<MinCut> MinCutAnalysisResult;
typedef std::vector<std::vector<fuzztree::ChildNode*>> IntermediateMOCUSResult;

class MinCutAnalysisTask
{
public:
	MinCutAnalysisTask(const fuzztree::TopEvent* topEvent, std::ofstream& logfile);
	~MinCutAnalysisTask();

	std::future<MinCutAnalysisResult> run();

protected:
	MinCutAnalysisResult analyze();
	void analyzeRecursive(IntermediateMOCUSResult&, const fuzztree::ChildNode&);

	static MinCutAnalysisResult minimizeResult(const IntermediateMOCUSResult&);

	const fuzztree::TopEvent* m_tree;

	std::ofstream& m_logFile;
};