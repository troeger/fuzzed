#include "MinCutAnalysisTask.h"
#include "FuzzTreeTypes.h"
#include "FatalException.h"

#include <limits>

using namespace fuzztree;
using std::vector;
using std::string;

namespace
{
	static const std::string UNDEVELOPED_ERROR	= "Cannot analyze trees with undeveloped events!";
	static const std::string UNKNOWN_TYPE		= "Unknown Child Node Type";
}


MinCutAnalysisTask::MinCutAnalysisTask(const TopEvent* const topEvent, std::ofstream& logfile)
	: m_tree(topEvent), m_logFile(logfile)
{}

MinCutAnalysisResult MinCutAnalysisTask::analyze()
{
	if (m_tree->children().size() == 0)
		return MinCutAnalysisResult();

	IntermediateMOCUSResult intermediateResult(1, 1);
	analyzeRecursive(intermediateResult, m_tree->children().front(), 0, 0);
	
	return minimizeResult(intermediateResult);
}

void MinCutAnalysisTask::analyzeRecursive(
	IntermediateMOCUSResult& results,
	const fuzztree::ChildNode& node,
	unsigned int row,
	unsigned int col)
{
	using namespace fuzztreeType;
	const type_info& typeName = typeid(node);
	
	// Leaf nodes...
	if (typeName == *BASICEVENT || typeName == *HOUSEEVENT || typeName == *UNDEVELOPEDEVENT) 
	{
		//assert(results.getHeight() >= row);
		results.set(row, col, &node);
	}
	else if (typeName == *BASICEVENTSET || typeName == *INTERMEDIATEEVENTSET)
	{
		// the java code handled this, so the event sets were not expanded by the configuration
		// the C++ configuration code already expands event sets
		const string error = string("Unexpected Event Set (they should have been removed by configuration): ") + typeName.name();
		m_logFile << error << std::endl;
		
		throw FatalException(error, 0, node.id());
	}
	else if (typeName == *INTERMEDIATEEVENT)
	{
		if (node.children().size() != 1)
		{
			m_logFile << "Intermediate Event size != 1, ID: , size: " << node.id() << std::endl;
			if (node.children().size() == 0) return;
		}
		analyzeRecursive(results, node.children().front(), row, col);
	}
	
	else if (typeName == *AND)
	{ // add a new column
		for (const auto& c : node.children())
		{
			results.addColumn();
			results.set(row, ++col, &c);
			analyzeRecursive(results, c, row, col);
		}
	}
	else if (typeName == *OR || typeName == *XOR || typeName == *VOTINGOR)
	{ // add a new row
		for (const auto& c : node.children())
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
			if (entry != nullptr && isLeaf(entry)) mc.emplace_back(entry->id());
		
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

bool MinCutAnalysisTask::isLeaf(const fuzztree::ChildNode* node)
{
	return dynamic_cast<const fuzztree::BasicEvent*>(node) != nullptr
		|| dynamic_cast<const fuzztree::HouseEvent*>(node) != nullptr
		|| dynamic_cast<const fuzztree::UndevelopedEvent*>(node) != nullptr;
}

MinCutAnalysisTask::~MinCutAnalysisTask()
{
	;
}