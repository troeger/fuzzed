#pragma once
#include "AbstractProbability.h"

class StaticProbability : public AbstractProbability
{
public:
	StaticProbability(double value) : AbstractProbability(), m_value(value) {};

	const double& getValue() const { return m_value;  }

protected:
	double m_value;
};