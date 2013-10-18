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
	FuzzTreeTransform(std::auto_ptr<fuzztree::FuzzTree> ft);

	~FuzzTreeTransform();

	void generateConfigurationsFile(const std::string& outputXML);
	std::vector<std::pair<FuzzTreeConfiguration, fuzztree::FuzzTree>> transform();

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

	// add the configured child gate, return true if leaf was reached
	bool handleFeatureVP(
		const fuzztree::ChildNode* templateNode,
		fuzztree::Node* node,
		const FuzzTreeConfiguration& configuration,
		const FuzzTreeConfiguration::id_type& configuredChildId) const;

	ErrorType expandBasicEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode, 
		const int& defaultQuantity = 0) const;

	ErrorType expandIntermediateEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode,
		const FuzzTreeConfiguration& configuration,
		const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	ErrorType generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static bool isOptional(const fuzztree::Node& node);
	static int parseCost(const fuzztree::InclusionVariationPoint& node);

	std::string generateUniqueId(const std::string& oldId);

	static xml_schema::Properties validationProperties(); // throwing an error. not used currently.
	
private:
	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
};