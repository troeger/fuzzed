#include "ConfigurationResultDocument.h"

namespace
{	
	const char* const CHOICE = "Choice";
	const char* const FEATURE_CHOICE= "FeatureChoice";
	const char* const REDUNDANCY_CHOICE = "RedundancyChoice";
	const char* const INCLUSION_CHOICE = "InclusionChoice";
	const char* const INCLUDED = "included";
	const char* const INT_TO_CHOICE	= "IntegerToChoiceMap";
}

ConfigurationResultDocument::ConfigurationResultDocument()
	: AbstractResultDocument("ConfigurationResult")
{}

void ConfigurationResultDocument::addConfigurations(const std::vector<FuzzTreeConfiguration>& configs)
{
	// first serialize the existing FuzzTree?


	// for each configuration, write only the Choice information
	for (const auto& config : configs)
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
}

pugi::xml_node ConfigurationResultDocument::choiceNode(FuzzTreeConfiguration::id_type ID)
{
	auto cm = m_root.append_child(INT_TO_CHOICE);
	cm.append_attribute("key").set_value(ID.c_str());

	return cm;
}
