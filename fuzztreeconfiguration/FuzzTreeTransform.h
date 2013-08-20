#pragma once

#include <string>
#include <set>
#include <iostream>

#include "platform.h"
#include "FuzzTreeConfiguration.h"

// generated model files
#include "faultTree.h"
#include "fuzzTree.h"

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

	std::vector<faulttree::FaultTree> transform();

protected:
	faulttree::FaultTree generateFaultTree(const FuzzTreeConfiguration& configuration);
	ErrorType generateFaultTreeRecursive(
		const fuzztree::Node* templateNode,
		faulttree::Node* node,
		const FuzzTreeConfiguration& configuration) const;

	static void copyNode(
		const std::string typeName,
		faulttree::Node* node,
		const std::string id,
		const fuzztree::ChildNode& currentChild);

	// add the configured VotingOR gate, return true if leaf was reached
	bool handleRedundancyVP(
		const fuzztree::ChildNode* templateNode,
		faulttree::Node* node,
		const std::tuple<int,int> configuredN,
		const FuzzTreeConfiguration::id_type& id) const;

	// add the configured child gate, return true if leaf was reached
	bool handleFeatureVP(
		const fuzztree::ChildNode* templateNode,
		faulttree::Node* node,
		const FuzzTreeConfiguration& configuration,
		const FuzzTreeConfiguration::id_type& configuredChildId) const;

	ErrorType expandBasicEventSet(
		const fuzztree::Node* templateNode,
		faulttree::Node* parentNode, 
		const FuzzTreeConfiguration::id_type& id,
		const int& defaultQuantity = 0) const;

	ErrorType expandIntermediateEventSet(
		const fuzztree::Node* templateNode,
		faulttree::Node* parentNode,
		const FuzzTreeConfiguration::id_type& id,
		const FuzzTreeConfiguration& configuration,
		const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	ErrorType generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static bool isOptional(const fuzztree::Node& node);
	static bool isGate(const std::string& node);
	static bool isLeaf(const std::string& node);
	static bool isVariationPoint(const std::string& node);
	static bool isEventSet(const std::string& node);

	static bool connectionRuleViolated(const std::string& parentType, const std::string& childType);
	
	std::string generateUniqueId(const std::string& oldId);
	
private:
	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
};