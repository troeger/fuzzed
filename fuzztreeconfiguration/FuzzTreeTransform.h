#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/path.hpp>
#include <string>
#include <set>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#include "platform.h"

// generated model files
#include "faultTree.h"
#include "fuzzTree.h"

struct FuzzTreeConfiguration;

class FuzzTreeTransform
{
public:
	// produces Fault Tree representations in memory. TODO return pointers?
	static std::vector<faulttree::FaultTree> transformFuzzTree(const std::string& fuzzTreeXML) noexcept;

protected:
	faulttree::FaultTree generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const fuzztree::Node* templateNode, /*Xerces*/
		faulttree::Node* node, /*generated internal fault tree model*/
		const FuzzTreeConfiguration& configuration) const;

	// returns the configured VotingOR gate
	std::pair<faulttree::ChildNode, bool /*isLeaf*/> handleRedundancyVP(
		const fuzztree::ChildNode* templateNode,
		faulttree::ChildNode* node,
		const std::tuple<int,int> configuredN, const int& id) const;

	// returns the configured child gate
	 std::pair<faulttree::ChildNode, bool /*isLeaf*/> handleFeatureVP(
		const fuzztree::ChildNode* templateNode,
		faulttree::ChildNode* node,
		const FuzzTreeConfiguration& configuration,
		const int configuredChildId) const;

	void expandBasicEventSet(
		const fuzztree::Node* templateNode, /*Xerces*/
		faulttree::Node* parentNode, /*generated internal fault tree model*/ 
		const int& id, const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	void generateConfigurationsRecursive(
		const fuzztree::Node* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static bool isOptional(const fuzztree::Node& node);
	static bool isGate(const fuzztree::Node& node);
	static bool isLeaf(const fuzztree::Node& node);
	
	static bool isDummy(const faulttree::Node& node);

	std::string generateUniqueId(const std::string& oldId);
	int generateUniqueId(int oldId);

private:
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	~FuzzTreeTransform();

	std::auto_ptr<fuzztree::FuzzTree> m_fuzzTree;

	int m_count;
};