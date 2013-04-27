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

class FuzzTreeConfiguration;

class FuzzTreeTransform : public XMLImport
{
public:
	// produces Fault Tree Files in targetDir
	static void transformFuzzTree(const std::string& fileName, const std::string& targetDir);

protected:
	void scheduleFTGeneration(boost::function<void()>& task);

	void generateFaultTree(const FuzzTreeConfiguration& configuration);
	void generateFaultTreeRecursive(xml_node& node, const FuzzTreeConfiguration& configuration);

	void generateConfigurations(vector<FuzzTreeConfiguration>& configurations);
	void generateConfigurationsRecursive(const xml_node& node, vector<FuzzTreeConfiguration>& configurations);

	static void shallowCopy(const xml_node& proto, xml_node& copiedNode);
	static bool isFaultTreeGate(const string& typeDescriptor);
	static bool isLeaf(const string& typeDescriptor);

	const std::string uniqueFileName();

private:
	FuzzTreeTransform(const string& fileName, const string& targetDir);
	virtual ~FuzzTreeTransform();

	virtual bool loadRootNode() override;
	
	boost::threadpool::fifo_pool m_threadPool;
	boost::filesystem::path m_targetDir; // where the differently configured trees end up

	int m_count;
};