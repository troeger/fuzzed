#pragma once

#include <string>
#include <set>
#include <iostream>
#include <fstream>

#include "platform.h"
#include "FuzzTreeConfiguration.h"
#include "Issue.h"

// generated model files
#include "Faulttree.h"
#include "Fuzztree.h"

enum ErrorType
{
	OK,
	WRONG_CHILD_TYPE,
	WRONG_CHILD_NUM,
	INVALID_NODE,
	INVALID_ATTRIBUTE
};

class FuzzTreeTransform
{
public:
	FuzzTreeTransform(const std::string& fuzzTreeXML, std::set<Issue>& errors);
	FuzzTreeTransform(std::istream& fuzzTreeXML, std::set<Issue>& errors);
	FuzzTreeTransform(std::auto_ptr<Fuzztree> ft, std::set<Issue>& errors);

	~FuzzTreeTransform();

	std::vector<std::pair<FuzzTreeConfiguration, Fuzztree>> transform();

	bool isValid() const { return m_bValid; }

protected:
	Fuzztree generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration);
	ErrorType generateVariationFreeFuzzTreeRecursive(
		const AbstractNode* templateNode,
		AbstractNode* node,
		const FuzzTreeConfiguration& configuration);

	static void copyNodeAsChild(
		AbstractNode* node,
		const std::string id,
		const AbstractNode& currentChild);

	// add the configured child gate, return true if leaf was reached
	bool handleFeatureVP(
		const AbstractNode* templateNode,
		AbstractNode* node,
		const FuzzTreeConfiguration& configuration,
		const FuzzTreeConfiguration::id_type& configuredChildId);

	ErrorType expandBasicEventSet(
		const AbstractNode* templateNode,
		AbstractNode* parentNode, 
		const int& defaultQuantity = 0);

	ErrorType expandIntermediateEventSet(
		const AbstractNode* templateNode,
		AbstractNode* parentNode,
		const FuzzTreeConfiguration& configuration,
		const int& defaultQuantity = 0);
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations);
	ErrorType generateConfigurationsRecursive(
		const AbstractNode* node, 
		std::vector<FuzzTreeConfiguration>& configurations,
		unsigned int& configCount);

	std::string generateUniqueId(const std::string& oldId);

private:
	std::auto_ptr<Fuzztree> m_fuzzTree;

	int m_count;
	bool m_bValid;

	std::set<Issue>& m_issues;
};