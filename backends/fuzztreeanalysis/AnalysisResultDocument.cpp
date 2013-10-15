#include "AnalysisResultDocument.h"

using namespace pugi;
using std::string;

namespace
{
	const char* const DURATION = "duration";
	const char* const DECOMPOSITIONNUMBER = "decompositionNumber";

	const char* const DECOMPOZEDFUZZYPROG = "DecomposedFuzzyProbability";
	const char* const CONFIGURATION = "configurations";
	const char* const ALPHACUTS = "alphaCuts";
	const char* const KEY = "key";
	const char* const VALUE = "value";
	const char* const PROBABILITY = "probability";

	const char* const NAMESPACE = ""; // TODO
}

AnalysisResultDocument::AnalysisResultDocument() : AbstractResultDocument("Analysis")
{}

void AnalysisResultDocument::setDecompositionNumber(const int& decompositionNum)
{
	m_root.append_attribute(DECOMPOSITIONNUMBER).set_value(decompositionNum);
}


void AnalysisResultDocument::addConfiguration(const DecomposedFuzzyInterval& prob)
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