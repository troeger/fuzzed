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
	void loadNode(const xml_node& node);

	void handleBasicEventSet(xml_node &child);
	void handleFeatureVP(xml_node &child);
	void handleRedundancyVP(xml_node &child);

private:
	FuzzTreeTransform(const string& fileName);
	virtual ~FuzzTreeTransform();

	virtual bool loadRootNode() override;
	
	boost::threadpool::pool m_threadPool;
};