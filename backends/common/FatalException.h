#pragma once
#include <stdexcept>
#include "Issue.h"

class FatalException : public std::runtime_error
{
	FatalException(const std::string msg, const int issueId = 0, const std::string elementId = "");

	const Issue& getIssue() const;

	virtual const char* what() const throw() override;

protected:
	Issue m_issue;

	std::string m_description;
};