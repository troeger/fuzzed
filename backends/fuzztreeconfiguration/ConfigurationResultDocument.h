#pragma once
#include "AbstractResultDocument.h"
#include "fuzztree.h"
#include <vector>

class ConfigurationResultDocument : public AbstractResultDocument
{
public:
	ConfigurationResultDocument();
	virtual ~ConfigurationResultDocument() {}

	void addConfigurations(const std::vector<FuzzTreeConfiguration>& configs);
	void addTreeSpecification(std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree);
};