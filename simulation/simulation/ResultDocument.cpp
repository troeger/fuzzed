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
	// TODO
}

void ResultDocument::addWarning(const std::string& message)
{
	// TODO
}

void ResultDocument::setModelId(const int& modelID)
{
	m_root.append_attribute(MODELID).set_value(modelID);
}

void ResultDocument::setTimeStamp(const int& timeStamp)
{
	m_root.append_attribute(TIMESTAMP).set_value(timeStamp);
}

void ResultDocument::setResults(
	const long double& reliability, 
	const long double& meanAvailability, 
	const long double& mttf, 
	const unsigned long& nRounds, 
	const unsigned long& nFailures,
	const long& duration)
{
	m_root.append_attribute(RELIABILITY).set_value((double)reliability);
	m_root.append_attribute(AVAILABILTIY).set_value((double)meanAvailability);
	m_root.append_attribute(MTTF).set_value((double)mttf);
	m_root.append_attribute(NROUNDS).set_value((long)nRounds);
	m_root.append_attribute(NFAILURES).set_value((long)nFailures);
	m_root.append_attribute(DURATION).set_value(duration);
}

bool ResultDocument::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}