#pragma once
#include "pugixml.hpp"
#include "DecomposedFuzzyInterval.h"

// TODO: make this similar to the ResultDocument.h from the simulation sources
class AnalysisResultDocument : public pugi::xml_document
{
public:
	AnalysisResultDocument();
	virtual ~AnalysisResultDocument() {}

	void addError(const std::string& message, const std::string& elementID);
	void addWarning(const std::string& message, const std::string& elementID);

	void setModelId(const std::string& modelID);
	void setTimeStamp(const int& timeStamp);
	void setDecompositionNumber(const int& decompositionNum);

	void addConfiguration(const DecomposedFuzzyInterval& prob);

	bool save(const std::string& fileName);

	bool valid() const { return !pugi::xml_document::empty(); }
	bool saved() const { return m_bSaved; }

protected:
	void initXML();

	pugi::xml_node m_root;
	bool m_bSaved;

	int m_warnings;
	int m_errors;
};