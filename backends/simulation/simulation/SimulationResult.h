#pragma once
#include "Result.h"

class SimulationResult : public Result
{
public:
	SimulationResult(std::string modelId, std::string id, std::string timestamp);

	double reliability;
	double meanAvailability;
	double mttf;
	unsigned int nRounds;
	unsigned int nFailures;
	double duration;

	const bool isValid() const override { return nRounds > 0; }

	const std::string getType() const override;
	void createXML(pugi::xml_node& resultNode) const override;
};