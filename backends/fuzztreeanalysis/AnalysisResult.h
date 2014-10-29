#pragma once
#include "Result.h"
#include "Probability.h"

class AnalysisResult : public Result
{
public:
	AnalysisResult(std::string modelId, std::string id, std::string timestamp, const DecomposedFuzzyInterval& analysisResult);

	const DecomposedFuzzyInterval& getAlphaCuts() const;

	const std::string getType() const override;
	void createXML(pugi::xml_node& resultNode) const override;

	const bool isValid() const;

private:
	const DecomposedFuzzyInterval m_analysisResult;
};