#include "AnalysisResult.h"

const DecomposedFuzzyInterval& AnalysisResult::getAlphaCuts() const
{
	return m_analysisResult;
}

AnalysisResult::AnalysisResult(std::string modelId, std::string id, std::string timestamp, const DecomposedFuzzyInterval& analysisResult)
: Result(modelId, id, timestamp), m_analysisResult(analysisResult)
{

}
