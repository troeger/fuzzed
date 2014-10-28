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
	Model faultTreeFromConfiguration(const FuzzTreeConfiguration& config);

	const std::set<Issue>& getIssues() const;

private:
	bool generateConfigurationsRecursive(
		const Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations,
		unsigned int& configCount);
	
	bool faultTreeFromConfigurationRecursive(const Node* templateNode, Node* node, const FuzzTreeConfiguration& configuration);

	bool expandBasicEventSet(const Node* child, Node* parent, const int& defaultQuantity=0);
	
	bool expandIntermediateEventSet(
		const Node* child, Node* parent,
		const FuzzTreeConfiguration& configuration /*this is needed for further recursive descent*/,
		const int& defaultQuantity = 0);
	
	bool handleFeatureVP(const Node* templateNode,
		Node* node,
		const FuzzTreeConfiguration& configuration,
		const FuzzTreeConfiguration::id_type& configuredChildId);

	const Model* m_model;
	std::set<Issue> m_issues;
};