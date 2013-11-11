#pragma once

#include <string>
#include <set>
#include <iostream>
#include <fstream>

#include "platform.h"
#include "FuzzTreeConfiguration.h"

// generated model files
#include "faulttree.h"
#include "fuzztree.h"

#define DEFAULT_LOG_FILE "errors.txt"

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
	FuzzTreeTransform(const std::string& fuzzTreeXML, std::ofstream& logFile = std::ofstream(DEFAULT_LOG_FILE));
	FuzzTreeTransform(std::istream& fuzzTreeXML, std::ofstream& logFile = std::ofstream(DEFAULT_LOG_FILE));
	FuzzTreeTransform(std::auto_ptr<fuzztree::FuzzTree> ft, std::ofstream& logFile = std::ofstream(DEFAULT_LOG_FILE));

	~FuzzTreeTransform();

	void generateConfigurationsFile(const std::string& outputXML);

	std::vector<std::pair<FuzzTreeConfiguration, fuzztree::FuzzTree>> transform();

	bool isValid() const { return m_bValid; }

protected:
	fuzztree::FuzzTree generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration);
	ErrorType generateVariationFreeFuzzTreeRecursive(
		const fuzztree::Node* templateNode,
		fuzztree::Node* node,
		const FuzzTreeConfiguration& configuration);

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
		const FuzzTreeConfiguration::id_type& configuredChildId);

	ErrorType expandBasicEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode, 
		const int& defaultQuantity = 0);

	ErrorType expandIntermediateEventSet(
		const fuzztree::Node* templateNode,
		fuzztree::Node* parentNode,
		const FuzzTreeConfiguration& configuration,
		const int& defaultQuantity = 0);
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations);
	ErrorType generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations);

	static bool isOptional(const fuzztree::Node& node);
	static int parseCost(const fuzztree::InclusionVariationPoint& node);

	std::string generateUniqueId(const std::string& oldId);

	static xml_schema::Properties validationProperties(); // throwing an error. not used currently.
	
private:
	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
	bool m_bValid;

	std::ofstream& m_logFile;
};