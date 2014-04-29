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

std::future<MinCutAnalysisResult> MinCutAnalysisTask::run()
{
	return std::async(std::launch::async, &MinCutAnalysisTask::analyze, this);
}

MinCutAnalysisResult MinCutAnalysisTask::analyze()
{
	if (m_tree->children().size() == 0)
		return MinCutAnalysisResult();

	IntermediateMOCUSResult intermediateResult;
	analyzeRecursive(intermediateResult, m_tree->children().front());
	
	return minimizeResult(intermediateResult);
}

void MinCutAnalysisTask::analyzeRecursive(IntermediateMOCUSResult& results, const fuzztree::ChildNode& node)
{
	using namespace fuzztreeType;
	const type_info& typeName = typeid(node);
	
	// Leaf nodes...
	if (typeName == *BASICEVENT || typeName == *HOUSEEVENT || typeName == *UNDEVELOPEDEVENT) 
	{
		
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
		analyzeRecursive(results, node.children().front());
	}
	
	else if (typeName == *AND)
	{
		for (const auto& c : node.children())
		{
			analyzeRecursive(results, c);
		}
	}
	else if (typeName == *OR || typeName == *XOR || typeName == *VOTINGOR)
	{
		for (const auto& c : node.children())
		{
			analyzeRecursive(results, c);
		}
	}
}

static MinCutAnalysisResult MinCutAnalysisTask::minimizeResult(const IntermediateMOCUSResult& res)
{
	return MinCutAnalysisResult();
}

MinCutAnalysisTask::~MinCutAnalysisTask()
{
	;
}