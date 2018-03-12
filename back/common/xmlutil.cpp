#include "xmlutil.h"

configurations::Configuration serializedConfiguration(const FuzzTreeConfiguration &c)
{
	configurations::Configuration conf(c.getId(), c.getCost());
	for (const auto& inclusionChoice : c.getOptionalNodes())
	{
		conf.choice().push_back(
			configurations::IntegerToChoiceMap(
			configurations::InclusionChoice(inclusionChoice.second),
			inclusionChoice.first));
	}

	for (const auto& redundancyChoice : c.getRedundancyNodes())
	{
		conf.choice().push_back(
			configurations::IntegerToChoiceMap(
			configurations::RedundancyChoice(std::get<1>(redundancyChoice.second)),
			redundancyChoice.first));
	}

	for (const auto& featureChoice : c.getFeaturedNodes())
	{
		conf.choice().push_back(
			configurations::IntegerToChoiceMap(
			configurations::FeatureChoice(featureChoice.second),
			featureChoice.first));
	}

	return conf;
}

