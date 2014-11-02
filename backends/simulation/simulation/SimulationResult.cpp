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
	resultNode.append_attribute("reliability").set_value(reliability);
	resultNode.append_attribute("mttf").set_value(mttf);
	resultNode.append_attribute("nFailures").set_value(nFailures);
	resultNode.append_attribute("nRounds").set_value(nRounds);
	resultNode.append_attribute("availability").set_value(meanAvailability);
	resultNode.append_attribute("duration").set_value(duration);
}
