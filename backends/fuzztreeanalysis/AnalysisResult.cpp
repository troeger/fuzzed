#include "AnalysisResult.h"

const DecomposedFuzzyInterval& AnalysisResult::getAlphaCuts() const
{
	return m_analysisResult;
}

AnalysisResult::AnalysisResult(std::string modelId, std::string id, std::string timestamp, const DecomposedFuzzyInterval& analysisResult)
: Result(modelId, id, timestamp), m_analysisResult(analysisResult)
{

}

const std::string AnalysisResult::getType() const
{
	return "ftr:AnalysisResult";
}

void AnalysisResult::createXML(pugi::xml_node& result) const
{
	pugi::xml_node probability = result.append_child();
	probability.set_name("probability");
	probability.append_attribute("xsi:type") = "ftc:DecomposedFuzzyProbability";

	for (const auto& alphaCut : m_analysisResult)
	{
		pugi::xml_node alphaCut_node = probability.append_child();
		alphaCut_node.set_name("alphaCuts");
		alphaCut_node.append_attribute("key") = alphaCut.first;

		const NumericInterval& bounds = alphaCut.second;
		pugi::xml_node value = alphaCut_node.append_child();
		value.set_name("value");
		value.append_attribute("lowerBounds") = bounds.lowerBound;
		value.append_attribute("upperBounds") = bounds.upperBound;
	}
}

const bool AnalysisResult::isValid() const
{
	return !m_analysisResult.empty();
}
