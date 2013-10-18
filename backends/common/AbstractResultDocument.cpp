#include "AbstractResultDocument.h"

#include <cassert>

using namespace pugi;
using std::string;

namespace
{	
	const char* const RESULT = "Result";
	
	const char* const RES_ERROR		= "Error";
	const char* const RES_WARNING	= "Warning";
	const char* const ISSUE_ID		= "issueId";
	const char* const ELEMENT_ID	= "elementId";
	const char* const MODELID		= "modelId";
	const char* const TIMESTAMP		= "timestamp";
	const char* const KEY = "key";
	const char* const VALUE = "value";
	
	// Configurations are part of every other result document.
	// Results are always per-config
	const char* const CHOICE = "Choice";
	const char* const FEATURE_CHOICE= "FeatureChoice";
	const char* const REDUNDANCY_CHOICE = "RedundancyChoice";
	const char* const INCLUSION_CHOICE = "InclusionChoice";
	const char* const INCLUDED = "included";
	const char* const INT_TO_CHOICE	= "IntegerToChoiceMap";

	const char* const NAMESPACE = ""; // TODO
}

AbstractResultDocument::AbstractResultDocument(const std::string prefix) : xml_document(),
	m_prefix(prefix)
{
	initXML();
}

void AbstractResultDocument::initXML()
{
	m_root = append_child(std::string(m_prefix + RESULT).c_str());
}

void AbstractResultDocument::addError(const string& msg, const string& elementID)
{
	auto errorNode = m_root.append_child(std::string(m_prefix + RES_ERROR).c_str());
	errorNode.append_attribute(ELEMENT_ID).set_value(elementID.c_str());
	errorNode.append_child(node_pcdata).set_value(msg.c_str());
	errorNode.append_attribute(ISSUE_ID).set_value(++m_errors);
}

void AbstractResultDocument::addWarning(const string& msg, const string& elementID)
{
	auto warningNode = m_root.append_child(std::string(m_prefix + RES_WARNING).c_str());
	warningNode.append_attribute(ELEMENT_ID).set_value(elementID.c_str());
	warningNode.append_child(node_pcdata).set_value(msg.c_str());
	warningNode.append_attribute(ISSUE_ID).set_value(++m_warnings);
}

void AbstractResultDocument::setModelId(const string& modelID)
{
	m_root.append_attribute(MODELID).set_value(modelID.c_str());
}

void AbstractResultDocument::setTimeStamp(const int& timeStamp)
{
	m_root.append_attribute(TIMESTAMP).set_value(timeStamp);
}

bool AbstractResultDocument::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}

void AbstractResultDocument::addConfiguration(const FuzzTreeConfiguration& config)
{
	for (const auto& inclusionChoice : config.m_optionalNodes)
	{
		auto cm = choiceNode(inclusionChoice.first);
		auto cn = cm.append_child(INCLUSION_CHOICE);
		cn.append_attribute(INCLUDED).set_value(inclusionChoice.second ? "true" : "false");
	}

	for (const auto& redundancyChoice : config.m_redundancyNodes)
	{
		auto cm = choiceNode(redundancyChoice.first);
		auto cn = cm.append_child(REDUNDANCY_CHOICE);
		cn.append_attribute("n").set_value(std::get<0>(redundancyChoice.second));
	}

	for (const auto& featureChoice : config.m_featureNodes)
	{
		auto cm = choiceNode(featureChoice.first);
		auto cn = cm.append_child(FEATURE_CHOICE);
		cn.append_attribute("featureId").set_value(featureChoice.second.c_str());
	}
}

pugi::xml_node AbstractResultDocument::choiceNode(FuzzTreeConfiguration::id_type ID)
{
	auto cm = m_root.append_child(INT_TO_CHOICE);
	cm.append_attribute("key").set_value(ID.c_str());
	return cm;
}

