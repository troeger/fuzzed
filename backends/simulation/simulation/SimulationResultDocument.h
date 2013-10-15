#pragma once
#include "AbstractResultDocument.h"
#include "ResultStruct.h"

class SimulationResultDocument : public AbstractResultDocument
{
public:
	SimulationResultDocument();
	virtual ~SimulationResultDocument() {}

	void setResult(const SimulationResult& result);
};