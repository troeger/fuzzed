#pragma once
#include <stdexcept>
#include "Issue.h"

/**
 * Class: FatalException
 * 
 * An exception class which is thrown whenever a problem is so fatal that the backend cannot deliver useful results.
 */
class FatalException : public std::runtime_error
{
public:
    FatalException(const std::string msg, const int issueId = 0, const std::string elementId = "");

	const Issue& getIssue() const;

	virtual const char* what() const throw() override;

protected: 
    Issue m_issue;

	std::string m_description;
};