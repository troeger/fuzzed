#pragma once
#include "Result.h"
#include "Probability.h"

class AnalysisResult : public Result
{
public:
	AnalysisResult(std::string modelId, std::string id, std::string timestamp, const DecomposedFuzzyInterval& analysisResult);

	const DecomposedFuzzyInterval& getAlphaCuts() const;

private:
	const DecomposedFuzzyInterval m_analysisResult;
};