#pragma once
#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/threadpool.hpp>
#include <string>
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
	void loadNode(const xml_node& node, xml_node& previous, xml_document& newDoc);

	void handleBasicEventSet(const xml_node& child, xml_node& previous, xml_document& newDoc);
	void handleFeatureVP(const xml_node& child, xml_node& previous, xml_document& newDoc);
	void handleRedundancyVP(const xml_node& child, xml_node& previous, xml_document& newDoc);

	static void shallowCopy(const xml_node& proto, xml_node& copiedNode);
	static bool isFaultTreeGate(const string& typeDescriptor);

private:
	FuzzTreeTransform(const string& fileName, const string& targetDir);
	virtual ~FuzzTreeTransform();

	virtual bool loadRootNode() override;
	
	boost::threadpool::pool m_threadPool;
	boost::filesystem::path m_targetDir; // where the differently configured trees end up

	int m_count;
};