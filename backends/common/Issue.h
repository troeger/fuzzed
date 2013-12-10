#pragma once

#include <string>
#include "commonTypes.h"

struct Issue
{
public:
	Issue() {} // take this compiler
	Issue(const std::string& msg, const int issueId = 0, const std::string elementId = "");

	bool operator ==(const Issue&b) const;
	bool operator <(const Issue&b) const;

	static Issue warningIssue(const std::string& msg, const int issueId = 0, const std::string elementId = "");
	static Issue fatalIssue(const std::string& msg, const int issueId = 0, const std::string elementId = "");

	commonTypes::Issue serialized() const;

	const std::string getMessage() const; 

protected:
	int m_issueId;
	std::string m_elementId;
	std::string m_message;
	bool m_bFatal;
};