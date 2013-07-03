#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/path.hpp>
#include <string>
#include <set>
#include <iostream>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#include "platform.h"
#include "FuzzTreeConfiguration.h"

// generated model files
#include "faultTree.h"
#include "fuzzTree.h"

class FuzzTreeTransform
{
public:
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	FuzzTreeTransform(std::istream& fuzzTreeXML);

	~FuzzTreeTransform();

	std::vector<faulttree::FaultTree> transform();

protected:
	faulttree::FaultTree generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const fuzztree::Node* templateNode,
		faulttree::Node* node,
		const FuzzTreeConfiguration& configuration) const;

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

	void expandBasicEventSet(
		const fuzztree::Node* templateNode, /*Xerces*/
		faulttree::Node* parentNode, /*generated internal fault tree model*/ 
		const FuzzTreeConfiguration::id_type& id,
		const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	void generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static bool isOptional(const fuzztree::Node& node);
	static bool isGate(const std::string& node);
	static bool isLeaf(const std::string& node);
	static bool isVariationPoint(const std::string& node);
	
	std::string generateUniqueId(const std::string& oldId);
	
private:
	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
};