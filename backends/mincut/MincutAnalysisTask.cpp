#include "MincutAnalysisTask.h"
#include "FatalException.h"

#include <limits>

using std::vector;
using std::string;

namespace
{
	static const std::string UNDEVELOPED_ERROR	= "Cannot analyze trees with undeveloped events!";
	static const std::string UNKNOWN_TYPE		= "Unknown Child Node Type";
}


MinCutAnalysisTask::MinCutAnalysisTask(const Node* const topEvent, std::ofstream& logfile)
	: m_tree(topEvent), m_logFile(logfile)
{}

MinCutAnalysisResult MinCutAnalysisTask::analyze()
{
	if (m_tree->getChildren().size() == 0)
		return MinCutAnalysisResult();

	IntermediateMOCUSResult intermediateResult(1, 1);
	analyzeRecursive(intermediateResult, m_tree->getChildren().front(), 0, 0);
	
	return minimizeResult(intermediateResult);
}

void MinCutAnalysisTask::analyzeRecursive(
	IntermediateMOCUSResult& results,
	const Node& node,
	unsigned int row,
	unsigned int col)
{
	const std::string& typeName = node.getType();
	
	// Leaf nodes...
	if (node.isLeaf()) 
	{
		//assert(results.getHeight() >= row);
		results.set(row, col, &node);
	}
	else if (node.isEventSet())
	{
		// the java code handled this, so the event sets were not expanded by the configuration
		// the C++ configuration code already expands event sets
		const string error = string("Unexpected Event Set (they should have been removed by configuration): ") + typeName;
		m_logFile << error << std::endl;
		
		throw FatalException(error, 0, node.getId());
	}
	else if (typeName == nodetype::INTERMEDIATEEVENT)
	{
		if (node.getChildren().size() != 1)
		{
			m_logFile << "Intermediate Event size != 1, ID: , size: " << node.getId() << std::endl;
			if (node.getChildren().size() == 0) return;
		}
		analyzeRecursive(results, node.getChildren().front(), row, col);
	}
	
	else if (typeName == nodetype::AND)
	{ // add a new column
		for (const auto& c : node.getChildren())
		{
			results.addColumn();
			results.set(row, ++col, &c);
			analyzeRecursive(results, c, row, col);
		}
	}
	else if (typeName == nodetype::OR || typeName == nodetype::XOR || typeName == nodetype::VOTINGOR)
	{ // add a new row
		for (const auto& c : node.getChildren())
		{
			results.addRow();
			results.set(++row, col, &c);
			analyzeRecursive(results, c, row, col);
		}
	}
}

MinCutAnalysisResult MinCutAnalysisTask::minimizeResult(const IntermediateMOCUSResult& res)
{
	unsigned int minCutLength = std::numeric_limits<unsigned int>::max();
	std::vector<MinCut> allCuts;
	std::vector<MinCut> minCuts;
	for (unsigned int r = 0; r < res.getHeight(); ++r)
	{
		const auto row = res.getRow(r);
		MinCut mc;
		for (const auto entry : row)
			if (entry != nullptr && entry->isLeaf()) mc.emplace_back(entry->getId());
		
		const auto rowLength = mc.size();
		if (rowLength == 0) continue;
		else if (rowLength < minCutLength)
		{
			minCutLength = rowLength;
			minCuts.clear();
			minCuts.emplace_back(mc);
		}
		else if (rowLength == minCutLength)
		{
			minCuts.emplace_back(mc);
		}
		allCuts.emplace_back(mc);
	}
	assert(allCuts.size() >= minCuts.size());
	return MinCutAnalysisResult(allCuts);
}

MinCutAnalysisTask::~MinCutAnalysisTask()
{
	;
}
