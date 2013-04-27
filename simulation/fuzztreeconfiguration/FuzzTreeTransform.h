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

#include "XMLImport.h"

class FuzzTreeTransform : public XMLImport
{
public:
	// produces Fault Tree Files in targetDir
	static void transformFuzzTree(const std::string& fileName, const std::string& targetDir);

protected:
	void loadTree();

	void loadNode(const xml_node& node, xml_node& previous, xml_document* doc, std::set<int> optIds);

	void loadNodeInBranch(const xml_node& node, xml_node& previous, xml_document* doc, std::set<int> optIds);

	void handleBasicEventSet(const xml_node& child, xml_node& previous, xml_document* doc);
	void handleFeatureVP(const xml_node& child, xml_node& previous, xml_document* doc);
	void handleRedundancyVP(const xml_node& child, xml_node& previous, xml_document* doc);

	static void shallowCopy(const xml_node& proto, xml_node& copiedNode);
	static bool isFaultTreeGate(const string& typeDescriptor);

private:
	FuzzTreeTransform(const string& fileName, const string& targetDir);
	virtual ~FuzzTreeTransform();

	virtual bool loadRootNode() override;
	
	boost::threadpool::fifo_pool m_threadPool;
	boost::filesystem::path m_targetDir; // where the differently configured trees end up

	int m_count;
};