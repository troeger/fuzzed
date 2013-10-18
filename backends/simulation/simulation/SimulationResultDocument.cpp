#include "SimulationResultDocument.h"
using std::string;
namespace simulation
{
	const char* const RELIABILITY = "reliability";
	const char* const AVAILABILTIY = "availability";
	const char* const NROUNDS = "nSimulatedRounds";
	const char* const MTTF = "mttf";
	const char* const NFAILURES = "nFailures";
	const char* const MODELID = "modelId";
	const char* const TIMESTAMP = "timestamp";
	const char* const DURATION = "duration";
}
using namespace simulation;

SimulationResultDocument::SimulationResultDocument() : AbstractResultDocument("Simulation")
{}

void SimulationResultDocument::setResult(const SimulationResult& result)
{
	m_root.append_attribute(RELIABILITY).set_value((double)result.reliability);
	m_root.append_attribute(AVAILABILTIY).set_value((double)result.meanAvailability);
	m_root.append_attribute(MTTF).set_value((double)result.mttf);
	m_root.append_attribute(NROUNDS).set_value(result.nRounds);
	m_root.append_attribute(NFAILURES).set_value(result.nFailures);
	m_root.append_attribute(DURATION).set_value(result.duration);
}

void SimulationResultDocument::addSimulationResult(
	const FuzzTreeConfiguration& config,
	const SimulationResult& result)
{
	auto confignode = AbstractResultDocument::addConfigurationNode(config, m_root);
	auto resultnode = confignode.append_child("result");

	resultnode.append_attribute(RELIABILITY).set_value((double)result.reliability);
	resultnode.append_attribute(AVAILABILTIY).set_value((double)result.meanAvailability);
	resultnode.append_attribute(MTTF).set_value((double)result.mttf);
	resultnode.append_attribute(NROUNDS).set_value(result.nRounds);
	resultnode.append_attribute(NFAILURES).set_value(result.nFailures);
	resultnode.append_attribute(DURATION).set_value(result.duration);
}
