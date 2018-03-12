#pragma once

#include <string>
#include "commonTypes.h"

/**
 * Class: Issue
 * A class representing a problem during the analysis of a model.
 */
struct Issue
{
public:
	Issue() {};
	Issue(const std::string& msg, const int issueId = 0, const std::string elementId = "");

	bool operator ==(const Issue&b) const;
	bool operator <(const Issue&b) const;

	/**
	 * Function: warningIssue
	 * Constructs an issue corresponding to a non-fatal warning.
	 *
	 * Parameters:
	 * 	msg - the warning message.
	 *	issueId - the warning identifier.
	 * 	elementId - the identifier of the graph element which the warning refers to.
	 */
	static Issue warningIssue(const std::string& msg, const int issueId = 0, const std::string elementId = "");

	/**
	 * Function: fatalIssue
	 * Constructs an issue corresponding to a fatal error.
	 *
	 * Parameters:
	 * 	msg - the error message.
	 *	issueId - the error identifier.
	 * 	elementId - the identifier of the graph element which the error refers to.
	 */
	static Issue fatalIssue(const std::string& msg, const int issueId = 0, const std::string elementId = "");

	commonTypes::Issue serialized() const;

	const std::string getMessage() const; 

protected:
	int m_issueId;
	std::string m_elementId;
	std::string m_message;
	bool m_bFatal;
};