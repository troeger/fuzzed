#include "SimulationResult.h"

SimulationResult::SimulationResult(std::string modelId, std::string id, std::string timestamp) : 
Result(modelId, id, timestamp), reliability(1.0), meanAvailability(1.0), mttf(-1.0), nRounds(0), nFailures(0), duration(0.0)
{

}

const std::string SimulationResult::getType() const
{
	return "ftr:SimulationResult";
}

void SimulationResult::createXML(pugi::xml_node& resultNode) const
{

}
