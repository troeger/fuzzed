#include "Condition.h"
#include <boost/lexical_cast.hpp>

Condition::Condition(int placeID, int val, ConditionType type)
	: m_initialized(true), m_placeID(placeID), m_value(val), m_type(type)
{}

Condition::Condition() : m_initialized(false)
{}

std::string Condition::asString() const
{
	if (!m_initialized)
		return "";

	std::string str = "p" + boost::lexical_cast<std::string>(m_placeID);
	switch (m_type)
	{
	case MORE:
		str += " > "; 
		break;
	case LESS:
		str += " < "; 
		break;
	case EQUAL:
		str += " == "; 
		break;
	case MORE_OR_EQUAL:
		str += " >= "; 
		break;
	case LESS_OR_EQUAL:
		str += " <= "; 
		break;
	}
	str += boost::lexical_cast<std::string>(m_value);

	return str;
}
