#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/path.hpp>
#include <xercesc/dom/DOMDocument.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
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

namespace fuzztree = ft;

class FuzzTreeTransform
{
public:
	// produces Fault Tree representations in memory. TODO return pointers?
	static std::vector<faulttree::FaultTree> transformFuzzTree(const std::string& fuzzTreeXML) noexcept;

protected:
	void generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const fuzztree::Node* templateNode, /*Xerces*/
		faulttree::Node* node, /*generated internal fault tree model*/
		const FuzzTreeConfiguration& configuration) const;

	// returns the configured VotingOR gate
	std::pair<faulttree::Node, bool /*isLeaf*/> handleRedundancyVP(
		const fuzztree::Node* templateNode,
		faulttree::Node* node,
		const std::tuple<int,int> configuredN, const int& id) const;

	// returns the configured child gate
	 std::pair<faulttree::Node, bool /*isLeaf*/> handleFeatureVP(
		const fuzztree::Node* templateNode,
		faulttree::Node* node,
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

	static inline bool isGate(const std::string& typeDescriptor);
	static inline bool isLeaf(const std::string& typeDescriptor);

	std::string generateUniqueId(const char* oldId);

private:
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	~FuzzTreeTransform();

	bool loadRootNode();

	xercesc::DOMDocument* m_document;
	std::unique_ptr<fuzztree::FuzzTree> m_fuzzTree;

	xercesc::XercesDOMParser m_parser;

	int m_count;
};