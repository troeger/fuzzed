#include "AnalysisResult.h"

using namespace pugi;
using std::string;

namespace
{
	const char* const ANALYSIS_RESULT = "AnalysisResult";
	const char* const ANALYSIS_ERROR = "AnalysisError";
	const char* const ANALYSIS_WARNING = "AnalysisWarning";
	const char* const ISSUE_ID = "issueId";
	const char* const ELEMENT_ID = "elementId";
	const char* const MODELID = "modelId";
	const char* const TIMESTAMP = "timestamp";
	const char* const DURATION = "duration";
	const char* const DECOMPOSITIONNUMBER = "decompositionNumber";

	const char* const DECOMPOZEDFUZZYPROG = "DecomposedFuzzyProbability";
	const char* const CONFIGURATION = "Configuration";
	const char* const ALPHACUTS = "alphaCuts";
	const char* const KEY = "key";
	const char* const VALUE = "value";
	const char* const PROBABILITY = "probability";

	const char* const NAMESPACE = ""; // TODO
}

AnalysisResult::AnalysisResult() : xml_document()
{
	initXML();
}

void AnalysisResult::initXML()
{
	m_root = append_child(ANALYSIS_RESULT);
}

void AnalysisResult::addError(const string& msg, const string& elementID)
{
	auto errorNode = m_root.append_child(ANALYSIS_ERROR);
	errorNode.append_attribute(ELEMENT_ID).set_value(elementID.c_str());
	errorNode.append_attribute(ISSUE_ID).set_value(++m_errors);
}

void AnalysisResult::addWarning(const string& msg, const string& elementID)
{
	auto warningNode = m_root.append_child(ANALYSIS_WARNING);
	warningNode.append_attribute(ELEMENT_ID).set_value(elementID.c_str());
	warningNode.append_attribute(ISSUE_ID).set_value(++m_warnings);
}

void AnalysisResult::setModelId(const string& modelID)
{
	m_root.append_attribute(MODELID).set_value(modelID.c_str());
}

void AnalysisResult::setTimeStamp(const int& timeStamp)
{
	m_root.append_attribute(TIMESTAMP).set_value(timeStamp);
}

void AnalysisResult::setDecompositionNumber(const int& decompositionNum)
{
	m_root.append_attribute(DECOMPOSITIONNUMBER).set_value(decompositionNum);
}

bool AnalysisResult::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}

void AnalysisResult::addConfiguration(const DecomposedFuzzyInterval& prob)
{
	auto confignode = m_root.append_child(CONFIGURATION);
	auto probnode = confignode.append_child(PROBABILITY);
	
	for (const auto& ac : prob)
	{
		auto alphaCuts = probnode.append_child(ALPHACUTS);
		alphaCuts.append_attribute(KEY).set_value(ac.first);

		const auto interval = ac.second;
		auto intervalNode = alphaCuts.append_child("Interval");
		intervalNode.append_attribute("lowerBound").set_value((double)interval.lowerBound);
		intervalNode.append_attribute("upperBound").set_value((double)interval.upperBound);
	}
}