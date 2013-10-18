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
	const char* const VALID			= "validResult";
	const char* const KEY			= "key";
	const char* const VALUE			= "value";
	const char* const COSTS			= "costs";
	
	// Configurations are part of every other result document.
	// Results are always per-config
	const char* const FEATURE_CHOICE= "FeatureChoice";
	const char* const REDUNDANCY_CHOICE = "RedundancyChoice";
	const char* const INCLUSION_CHOICE = "InclusionChoice";
	const char* const INCLUDED = "included";
	const char* const CHOICES	= "choices";

	const char* const NAMESPACE = ""; // TODO
}

AbstractResultDocument::AbstractResultDocument(const std::string prefix) : xml_document(),
	m_prefix(prefix),
	m_issues(0)
{
	initXML();
}

void AbstractResultDocument::initXML()
{
	m_root = append_child(std::string(m_prefix + RESULT).c_str());
}

void AbstractResultDocument::addIssue(const string& msg, const string& elementID)
{
	auto issueNode = m_root.append_child("issues");
	issueNode.append_attribute(ELEMENT_ID).set_value(elementID.c_str());
	issueNode.append_child(node_pcdata).set_value(msg.c_str());
	issueNode.append_attribute(ISSUE_ID).set_value(++m_issues);
}

void AbstractResultDocument::setModelId(const string& modelID)
{
	m_root.append_attribute(MODELID).set_value(modelID.c_str());
}

void AbstractResultDocument::setTimeStamp(const string& timeStamp)
{
	m_root.append_attribute(TIMESTAMP).set_value(timeStamp.c_str());
}

bool AbstractResultDocument::save(const string& fileName)
{
	m_bSaved = xml_document::save_file(fileName.c_str());
	return m_bSaved;
}

pugi::xml_node AbstractResultDocument::addConfigurationNode(
	const FuzzTreeConfiguration &config,
	xml_node& parent)
{
	xml_node configNode = parent.append_child("configurations");
	configNode.append_attribute(COSTS).set_value(config.getCost());
	
	for (const auto& inclusionChoice : config.m_optionalNodes)
	{
		auto cm = choiceNode(inclusionChoice.first, configNode);
		auto cn = cm.append_child(VALUE);
		cn.append_attribute(INCLUDED).set_value(inclusionChoice.second ? "true" : "false");
	}

	for (const auto& redundancyChoice : config.m_redundancyNodes)
	{
		auto cm = choiceNode(redundancyChoice.first, configNode);
		auto cn = cm.append_child(VALUE);
		cn.append_attribute("n").set_value(std::get<0>(redundancyChoice.second));
	}

	for (const auto& featureChoice : config.m_featureNodes)
	{
		auto cm = choiceNode(featureChoice.first, configNode);
		auto cn = cm.append_child(VALUE);
		cn.append_attribute("featureId").set_value(featureChoice.second.c_str());
	}

	return configNode;
}

pugi::xml_node AbstractResultDocument::choiceNode(FuzzTreeConfiguration::id_type ID, xml_node& parent)
{
	auto cm = parent.append_child(CHOICES);
	cm.append_attribute("key").set_value(ID.c_str());
	return cm;
}

void AbstractResultDocument::setValid(bool valid)
{
	m_root.append_attribute(VALID).set_value(valid);
}

