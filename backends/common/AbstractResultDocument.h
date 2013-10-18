#pragma once
#include "pugixml.hpp"
#include "FuzzTreeConfiguration.h"

class AbstractResultDocument : public pugi::xml_document
{
public:
	AbstractResultDocument(const std::string prefix);
	virtual ~AbstractResultDocument() {}

	void addError(const std::string& message, const std::string& elementID);
	void addWarning(const std::string& message, const std::string& elementID);

	void setModelId(const std::string& modelID);
	void setTimeStamp(const std::string& timeStamp);

	bool save(const std::string& fileName);

	bool valid() const { return !pugi::xml_document::empty(); }
	bool saved() const { return m_bSaved; }

	xml_node addConfigurationNode(const FuzzTreeConfiguration &config, xml_node& parent);

protected:
	pugi::xml_node choiceNode(FuzzTreeConfiguration::id_type ID, xml_node& parent);
	
	void initXML();

	pugi::xml_node m_root;
	bool m_bSaved;

	int m_warnings;
	int m_errors;

	std::string m_prefix;
};