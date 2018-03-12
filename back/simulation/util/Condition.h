#pragma once
#include "Types.h"

/**
 * Class: Condition
 *
 * A boolean condition on a petri net marking.
 */
class Condition
{
public:
	Condition();
	Condition(int placeID, int val, ConditionType type);

	bool valid() const { return m_initialized; };
	bool isSatisfied() const;

	std::string asString() const;

private:
	bool m_initialized;

	int m_placeID;
	int m_value;

	ConditionType m_type;
};