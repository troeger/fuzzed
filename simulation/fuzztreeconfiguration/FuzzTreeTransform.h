#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/threadpool.hpp>
#include <string>
#include <set>
#if IS_WINDOWS 
#pragma warning(pop) 
#endif

#define HAS_CHILDREN(node) (!node.child("children").empty())
#define SET_OPTIONAL_FALSE(node) (node.remove_attribute(OPTIONAL_ATTRIBUTE))

#include "XMLImport.h"

struct FuzzTreeConfiguration;

class FuzzTreeTransform : public XMLImport
{
public:
	// produces Fault Tree Files in targetDir
	static void transformFuzzTree(const std::string& fileName, const std::string& targetDir);

protected:
	void scheduleFTGeneration(boost::function<void()>& task);

	void generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(
		const xml_node& templateNode, 
		xml_node& node,
		const FuzzTreeConfiguration& configuration) const;

	// returns the configured VotingOR gate
	pair<xml_node, bool /*isLeaf*/> handleRedundancyVP(
		const xml_node& templateNode, 
		xml_node& node, 
		const tuple<int,int> configuredN, const int& id) const;

	// returns the configured child gate
	pair<xml_node, bool /*isLeaf*/> handleFeatureVP(
		const xml_node& templateNode, 
		xml_node& node, 
		const int configuredChildId) const;

	void expandBasicEventSet(const xml_node& templateNode, xml_node& parent, const int& id, const int& defaultQuantity) const;
	
	void generateConfigurations(vector<FuzzTreeConfiguration>& configurations) const;
	void generateConfigurationsRecursive(
		const xml_node& node, 
		vector<FuzzTreeConfiguration>& configurations) const;

	static void shallowCopy(const xml_node& proto, xml_node& copiedNode);
	static bool isGate(const string& typeDescriptor);
	static bool isLeaf(const string& typeDescriptor);

	static int parseID(const xml_node& node);

	const std::string uniqueFileName();

private:
	FuzzTreeTransform(const string& fileName, const string& targetDir);
	virtual ~FuzzTreeTransform();

	virtual bool loadRootNode() override;
	
	boost::threadpool::fifo_pool m_threadPool;
	boost::filesystem::path m_targetDir; // where the differently configured trees end up

	int m_count;
};