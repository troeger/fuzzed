#pragma once
#include "AbstractResultDocument.h"
#include "ResultStruct.h"

class SimulationResultDocument
{
public:
	SimulationResultDocument();
	virtual ~SimulationResultDocument() {}

	void setResult(const SimulationResult& result);
	void addSimulationResult(const FuzzTreeConfiguration& config, const SimulationResult& prob);
};