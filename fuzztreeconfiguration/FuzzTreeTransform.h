#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <boost/filesystem/path.hpp>
#include <string>
#include <set>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/dom/DOMDocument.hpp>
#include <xercesc/dom/DOMNode.hpp>
#include <xercesc/dom/DOMDocumentType.hpp>
#include <xercesc/dom/DOMElement.hpp>
#include <xercesc/dom/DOMImplementation.hpp>
#include <xercesc/dom/DOMImplementationLS.hpp>
#include <xercesc/dom/DOMNodeIterator.hpp>
#include <xercesc/dom/DOMNodeList.hpp>
#include <xercesc/dom/DOMText.hpp>
#include <xercesc/util/XMLUni.hpp>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#include "platform.h"
#include "FaultTree.h"

struct FuzzTreeConfiguration;

using namespace xercesc;

class FuzzTreeTransform
{
public:
	// produces Fault Tree representations in memory. TODO return pointers?
	static std::vector<ft::FaultTree> transformFuzzTree(const std::string& fuzzTreeXML) noexcept;

protected:
	void generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const DOMNode* templateNode, /*Xerces*/
		ft::Node* node, /*generated internal fault tree model*/
		const FuzzTreeConfiguration& configuration) const;

	static void removeEmptyNodes(ft::Node* node);

	// returns the configured VotingOR gate
	std::pair<ft::Node, bool /*isLeaf*/> handleRedundancyVP(
		const DOMNode* templateNode, /*Xerces*/
		ft::Node* node, /*generated internal fault tree model*/
		const std::tuple<int,int> configuredN, const int& id) const;

	// returns the configured child gate
	 std::pair<ft::Node, bool /*isLeaf*/> handleFeatureVP(
		const DOMNode* templateNode, /*Xerces*/
		ft::Node* node, /*generated internal fault tree model*/
		const FuzzTreeConfiguration& configuration,
		const int configuredChildId) const;

	void expandBasicEventSet(
		const DOMNode* templateNode, /*Xerces*/
		ft::Node* parentNode, /*generated internal fault tree model*/ 
		const int& id, const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	void generateConfigurationsRecursive(
		const DOMNode* node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static inline bool isGate(const std::string& typeDescriptor);
	static inline bool isLeaf(const std::string& typeDescriptor);

	static int parseID(const DOMNode* node);

	std::string generateUniqueId(const char* oldId);

private:
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	~FuzzTreeTransform();

	bool loadRootNode();

	DOMDocument* m_document;
	DOMNode* m_rootNode;

	XercesDOMParser m_parser;

	int m_count;
};