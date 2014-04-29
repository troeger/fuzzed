#include "MinCutAnalysisTask.h"
#include "FuzzTreeTypes.h"
#include "xmlutil.h"
#include "FatalException.h"

#include <math.h>
#include <algorithm>
#include <bitset>
#include <climits>
#include <exception>

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

	IntermediateMOCUSResult intermediateResult(0, 0);
	intermediateResult.set(0, 0, dynamic_cast<const fuzztree::Node* const>(m_tree));
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
		assert(results.getHeight() >= row);
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
	{ // Add a new column
		results.addColumn();
		results.set(row, ++col, &node);
		for (const auto& c : node.children())
		{
			analyzeRecursive(results, c, row, col);
		}
	}
	else if (typeName == *OR || typeName == *XOR || typeName == *VOTINGOR)
	{ // add a new row
		results.addRow();
		results.set(++row, col, &node);
		for (const auto& c : node.children())
		{
			analyzeRecursive(results, c, row, col);
		}
	}
}

MinCutAnalysisResult MinCutAnalysisTask::minimizeResult(const IntermediateMOCUSResult& res)
{
	return MinCutAnalysisResult();
}

MinCutAnalysisTask::~MinCutAnalysisTask()
{
	;
}