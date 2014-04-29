#pragma once
#include "fuzztree.h"
#include "Dynamic2dArray.h"
#include <future>
#include <vector>

#include <fstream>

typedef std::vector<std::string> MinCut;
typedef std::vector<MinCut> MinCutAnalysisResult;
//typedef std::vector<std::vector<const fuzztree::Node*>> IntermediateMOCUSResult;
typedef Dynamic2dArray<const fuzztree::Node*> IntermediateMOCUSResult;

class MinCutAnalysisTask
{
public:
	MinCutAnalysisTask(const fuzztree::TopEvent* const topEvent, std::ofstream& logfile);
	~MinCutAnalysisTask();

	MinCutAnalysisResult analyze();

protected:
	void analyzeRecursive(IntermediateMOCUSResult&, const fuzztree::ChildNode&, unsigned int r, unsigned int c);

	static MinCutAnalysisResult minimizeResult(const IntermediateMOCUSResult&);

	const fuzztree::TopEvent* const m_tree;

	std::ofstream& m_logFile;
};