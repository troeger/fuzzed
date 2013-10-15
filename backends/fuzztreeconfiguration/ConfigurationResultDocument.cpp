#include "ConfigurationResultDocument.h"

ConfigurationResultDocument::ConfigurationResultDocument()
	: AbstractResultDocument("ConfigurationResult")
{

}

void ConfigurationResultDocument::addConfigurations(const std::vector<FuzzTreeConfiguration>& configs)
{
	// first serialize the existing FuzzTree?


	// for each configuration, write only the Choice information
	for (const auto& config : configs)
	{

	}
}
