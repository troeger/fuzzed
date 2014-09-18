#include "FatalException.h"
#include <sstream>
using std::endl;

FatalException::FatalException(const std::string msg, const int issueId /*= 0*/, const std::string elementId /*= ""*/)
	: std::runtime_error(msg), m_issue(Issue::fatalIssue(msg, issueId, elementId))
{
	std::stringstream description;
	description << 
		"Backend Issue: " <<
		msg << endl <<
		"IssueID: " << issueId << endl <<
		"ElementID: " << elementId << endl;

	m_description = description.str();
}

const char* FatalException::what() const throw() 
{
	return m_description.c_str();
}

const Issue& FatalException::getIssue() const
{
	return m_issue;
}
