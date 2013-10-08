#include "ResultDocument.h"
#include "Constants.h"

using namespace pugi;
using std::string;
using namespace simulation;

ResultDocument::ResultDocument() : xml_document()
{
	initXML();
}

void ResultDocument::initXML()
{
	m_root = append_child(SIMULATION_RESULT);
}

void ResultDocument::addError(const string& msg)
{
	auto errorNode = m_root.append_child(SIMULATION_ERROR);
	errorNode.append_attribute(SIMULATION_MESSAGE).set_value(msg.c_str());
	errorNode.append_attribute(ID_ATTRIBUTE).set_value(++m_errors);
}

void ResultDocument::addWarning(const string& msg)
{
	auto warningNode = m_root.append_child(SIMULATION_WARNING);
	warningNode.append_attribute(SIMULATION_MESSAGE).set_value(msg.c_str());
	warningNode.append_attribute(ID_ATTRIBUTE).set_value(++m_warnings);
}

void ResultDocument::setModelId(const int& modelID)
{
	m_root.append_attribute(MODELID).set_value(modelID);
}

void ResultDocument::setTimeStamp(const int& timeStamp)
{
	m_root.append_attribute(TIMESTAMP).set_value(timeStamp);
}

bool ResultDocument::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}

void ResultDocument::setResult(const SimulationResult& result)
{
	m_root.append_attribute(RELIABILITY).set_value((double)result.reliability);
	m_root.append_attribute(AVAILABILTIY).set_value((double)result.meanAvailability);
	m_root.append_attribute(MTTF).set_value((double)result.mttf);
	m_root.append_attribute(NROUNDS).set_value(result.nRounds);
	m_root.append_attribute(NFAILURES).set_value(result.nFailures);
	m_root.append_attribute(DURATION).set_value(result.duration);
}
