#pragma once
#include <string>

enum NodeType
{
	PLACE = 0,
	TRANSITION,
	ARC
};

enum TransitionType
{
	TIMED = 0,
	IMMEDIATE
};

enum ArcDirection
{
	PLACE_TO_TRANSITION = 0,
	TRANSITION_TO_PLACE
};

enum ConditionType
{
	MORE,
	LESS,
	EQUAL,
	MORE_OR_EQUAL,
	LESS_OR_EQUAL
};

inline std::string conditionTypeString(ConditionType cond) 
{
	switch (cond)
	{
	case EQUAL:
		return "==";
	case LESS:
		return "<";
	case LESS_OR_EQUAL:
		return "<=";
	case MORE_OR_EQUAL:
		return ">=";
	case MORE:
		return ">";
	}
	return "";
}