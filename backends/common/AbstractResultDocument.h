#pragma once
#include "pugixml.hpp"

class AbstractResultDocument : public pugi::xml_document
{
public:
	AbstractResultDocument(const std::string prefix);
	virtual ~AbstractResultDocument() {}

	void addError(const std::string& message, const std::string& elementID);
	void addWarning(const std::string& message, const std::string& elementID);

	void setModelId(const std::string& modelID);
	void setTimeStamp(const int& timeStamp);

	bool save(const std::string& fileName);

	bool valid() const { return !pugi::xml_document::empty(); }
	bool saved() const { return m_bSaved; }

protected:
	void initXML();

	pugi::xml_node m_root;
	bool m_bSaved;

	int m_warnings;
	int m_errors;

	std::string m_prefix;
};