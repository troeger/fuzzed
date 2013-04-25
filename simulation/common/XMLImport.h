#pragma once
#include <pugixml.hpp>

#ifdef __linux
	#include <pugixml.cpp>
#endif
#include <boost/filesystem/path.hpp>

using namespace std;
using namespace pugi;

/************************************************************************/
/* Abstract XML File importer.											*/
/* Subclassed by FuzzTreeImport and PNMLImport							*/
/************************************************************************/
class XMLImport
{
public:
	bool isLoaded() const { return m_bLoaded; };

protected:
	XMLImport(const string& fileName);
	
	bool validateAndLoad();
	virtual bool loadRootNode() = 0;
	
	boost::filesystem::path m_file;

	xml_document m_document;
	xml_node m_rootNode;

	bool m_bLoaded;
};