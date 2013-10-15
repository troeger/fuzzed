#pragma once
#include "AbstractResultDocument.h"
#include "FuzzTreeConfiguration.h"
#include <vector>

class ConfigurationResultDocument : public AbstractResultDocument
{
public:
	ConfigurationResultDocument();
	virtual ~ConfigurationResultDocument() {}

	void addConfigurations(const std::vector<FuzzTreeConfiguration>& configs);

protected:
	pugi::xml_node choiceNode(FuzzTreeConfiguration::id_type ID);
};