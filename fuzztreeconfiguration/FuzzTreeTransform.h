#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>
#include <string>
#include <set>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#define HAS_CHILDREN(node) (!node.child("children").empty())
#define SET_OPTIONAL_FALSE(node) (node.remove_attribute(OPTIONAL_ATTRIBUTE))

#include "platform.h"

struct FuzzTreeConfiguration;

class FuzzTreeTransform
{
public:
	// produces Fault Tree Files in targetDir
	static void transformFuzzTree(const std::string& fuzzTreeXML) noexcept;

protected:
	void generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const pugi::xml_node& templateNode, 
		pugi::xml_node& node,
		const FuzzTreeConfiguration& configuration) const;

	static void removeEmptyNodes(pugi::xml_node& node);

	// returns the configured VotingOR gate
	std::pair<pugi::xml_node, bool /*isLeaf*/> handleRedundancyVP(
		const pugi::xml_node& templateNode, 
		pugi::xml_node& node,
		const std::tuple<int,int> configuredN, const int& id) const;

	// returns the configured child gate
	 std::pair<pugi::xml_node, bool /*isLeaf*/> handleFeatureVP(
		const pugi::xml_node& templateNode, 
		pugi::xml_node& node,
		const FuzzTreeConfiguration& configuration,
		const int configuredChildId) const;

	void expandBasicEventSet(const pugi::xml_node& templateNode, pugi::xml_node& parent, const int& id, const int& defaultQuantity = 0) const;
	
	void generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const;
	void generateConfigurationsRecursive(
		const pugi::xml_node& node, 
		std::vector<FuzzTreeConfiguration>& configurations) const;

	static void shallowCopy(const pugi::xml_node& proto, pugi::xml_node& copiedNode);
	static bool isGate(const std::string& typeDescriptor);
	static bool isLeaf(const std::string& typeDescriptor);

	static int parseID(const pugi::xml_node& node);

	std::string generateUniqueId(const char* oldId);

private:
	FuzzTreeTransform(const std::string& fuzzTreeXML);
	~FuzzTreeTransform();

	bool loadRootNode();
	
	boost::filesystem::path m_targetDir; // where the differently configured trees end up

	pugi::xml_document m_document;
	pugi::xml_node m_rootNode;

	int m_count;
};