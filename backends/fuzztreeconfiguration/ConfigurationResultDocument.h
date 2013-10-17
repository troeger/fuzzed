#pragma once
#include "AbstractResultDocument.h"
#include "FuzzTreeConfiguration.h"
#include "fuzztree.h"
#include <vector>

class ConfigurationResultDocument : public AbstractResultDocument
{
public:
	ConfigurationResultDocument();
	virtual ~ConfigurationResultDocument() {}

	void addConfigurations(const std::vector<FuzzTreeConfiguration>& configs);
	void addTreeSpecification(std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree);

protected:
	pugi::xml_node choiceNode(FuzzTreeConfiguration::id_type ID);
};