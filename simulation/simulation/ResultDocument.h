#pragma once

#if IS_WINDOWS 
#pragma warning(push, 3) 
#endif
#include "pugixml.hpp"
#if IS_WINDOWS 
#pragma warning(pop)
#endif

class ResultDocument : public pugi::xml_document
{
public:
	ResultDocument();
	virtual ~ResultDocument() {}

	void addError(const std::string& message);
	void addWarning(const std::string& message);

	void setModelId(const int& modelID);
	void setTimeStamp(const int& timeStamp);
	void setResults(
		const long double& reliability, 
		const long double& meanAvailability, 
		const long double& mttf,
		const unsigned long& nRounds,
		const unsigned long& nFailures,
		const long& duration);

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