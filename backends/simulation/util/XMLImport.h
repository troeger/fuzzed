#pragma once
#include <pugixml.hpp>

#ifdef __linux
	#include <pugixml.cpp>
#endif
#include <boost/filesystem/path.hpp>

/**
 * Class: XMLImport
 *
 * A utility class for loading XML documents using pugixml.
 */
class XMLImport
{
public:
	bool isLoaded() const { return m_bLoaded; };

protected:
	XMLImport(const std::string& fileName);
	
	bool validateAndLoad();
	virtual bool loadRootNode() = 0;
	
	boost::filesystem::path m_file;

	pugi::xml_document m_document;
	pugi::xml_node m_rootNode;

	bool m_bLoaded;
};