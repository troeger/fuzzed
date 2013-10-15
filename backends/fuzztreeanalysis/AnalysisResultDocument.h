#pragma once
#include "AbstractResultDocument.h"
#include "DecomposedFuzzyInterval.h"

class AnalysisResultDocument : public AbstractResultDocument
{
public:
	AnalysisResultDocument();
	virtual ~AnalysisResultDocument() {}

	void setDecompositionNumber(const int& decompositionNum);
	void addConfiguration(const DecomposedFuzzyInterval& prob);
};