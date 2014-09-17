#pragma once
#include <set>
#include "FuzzTreeConfiguration.h"
#include "Model.h"
#include "Issue.h"

class FuzzTreeToFaultTree
{
public:
	FuzzTreeToFaultTree(const Model* model) : m_model(model) { assert(model->getType() == modeltype::FUZZTREE); };
	
	std::vector<FuzzTreeConfiguration> generateConfigurations();
	Model faultTreeFromConfiguration(const FuzzTreeConfiguration& config) const;

private:
	bool generateConfigurationsRecursive(
		const Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations,
		unsigned int& configCount);

	const Model* m_model;
	std::set<Issue> m_issues;
};