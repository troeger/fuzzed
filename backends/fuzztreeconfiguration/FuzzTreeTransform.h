#pragma once

#include <string>
#include <set>
#include <iostream>

#include "platform.h"
#include "FuzzTreeConfiguration.h"

// generated model files
#include "faulttree.h"
#include "fuzztree.h"

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
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	FuzzTreeTransform(std::istream& fuzzTreeXML);

	~FuzzTreeTransform();

	std::vector<fuzztree::FuzzTree> transform();

protected:
	fuzztree::FuzzTree generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration);
	ErrorType generateVariationFreeFuzzTreeRecursive(
		const fuzztree::Node* templateNode,
		fuzztree::Node* node,
		const FuzzTreeConfiguration& configuration) const;

	static void copyNode(
		const std::type_info& typeName,
		fuzztree::Node* node,
		const std::string id,
		const fuzztree::ChildNode& currentChild);

	// add the configured VotingOR gate, return true if leaf was reached
	bool handleRedundancyVP(
		const fuzztree::ChildNode* templateNode,
		fuzztree::Node* node,
		const std::tuple<int,int> configuredN,
		const FuzzTreeConfiguration::id_type& id) const;

	// add the configured child gate, return true if leaf was reached
	bool handleFeatureVP(
		const fuzztree::ChildNode* templateNode,
		fuzztree::Node* node,
		const FuzzTreeConfiguration& configuration,
		const FuzzTreeConfiguration::id_type& configuredChildId) const;

	ErrorType expandBasicEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode, 
		const FuzzTreeConfiguration::id_type& id,
		const int& defaultQuantity = 0) const;

	ErrorType expandIntermediateEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode,
		const FuzzTreeConfiguration::id_type& id,
		const FuzzTreeConfiguration& configuration,
		const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	ErrorType generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static bool isOptional(const fuzztree::Node& node);

	std::string generateUniqueId(const std::string& oldId);
	
private:
	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
};