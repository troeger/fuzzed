#include "Issue.h"

Issue Issue::warningIssue(const std::string& msg, const int issueId /*= 0*/, const std::string elementId /*= ""*/)
{
	Issue i(msg, issueId, elementId);
	i.m_bFatal = false;
	return i;
}

Issue Issue::fatalIssue(const std::string& msg, const int issueId /*= 0*/, const std::string elementId /*= ""*/)
{
	Issue i(msg, issueId, elementId);
	i.m_bFatal = true;
	return i;
}


Issue::Issue(const std::string& msg, const int issueId /*= 0*/, const std::string elementId /*= ""*/) :
	m_issueId(issueId), 
	m_elementId(elementId),
	m_bFatal(false),
	m_message(msg)
{

}

// commonTypes::Issue Issue::serialized() const
// {
// 	commonTypes::Issue i;
// 	i.message(m_message);
// 	i.isFatal(m_bFatal);
// 	i.elementId(m_elementId);
// 	i.issueId(m_issueId);
// 
// 	return i;
// }

const std::string Issue::getMessage() const
{
	return m_message;
}

bool Issue::operator==(const Issue&b) const
{
	return
		b.m_message == m_message &&
		b.m_elementId == m_elementId &&
		b.m_issueId == m_issueId;
}

bool Issue::operator<(const Issue&b) const
{
	return m_message.length() < b.m_message.length();
}
