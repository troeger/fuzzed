#include "Probability.h"
#include "util.h"
#include <cassert>
#include "FatalException.h"

Probability Probability::fromDescriptionString(const std::string descriptionString, const unsigned int missionTime)
{
	const std::string probTypeId = descriptionString.substr(0, 1);
	std::string probabilityDescriptor = util::insideBrackets(descriptionString);
	double val = atof(util::afterComma(probabilityDescriptor).c_str());

	if (probTypeId == "0") // static probability
	{
		// std::cout << probabilityDescriptor;
		if (probabilityDescriptor.find("[") != -1)
		{
		}
		return staticProbability(val, missionTime);
	}
	else if (probTypeId == "1")
	{
		return rateProbability(val, missionTime);
	}
	else if (probTypeId == "2")// fuzzy
	{
		//[0, [b1 = b2, b1 - a = c - b1]]
		std::string b = probabilityDescriptor.substr(0, probabilityDescriptor.find_first_of(","));
		return triangularFuzzyProbability(val, atof(b.c_str()), atof(b.c_str()), val, missionTime);
	}

	throw FatalException("Could not parse probability.");
}

Probability Probability::staticProbability(const double staticValue, const unsigned int missionTime)
{
	Probability p(probabilitytype::STATIC);
	p.m_staticValue = staticValue;
	p.m_missionTime = missionTime;

	p.m_rateValue = util::rateFromProbability(staticValue, missionTime);
	return p;
}

Probability Probability::rateProbability(const double rateValue, const unsigned int missionTime)
{
	Probability p(probabilitytype::RATE);
	p.m_rateValue = rateValue;

	p.m_missionTime = missionTime;
	p.m_staticValue = util::probabilityFromRate(rateValue, missionTime);
	return p;
}

Probability Probability::triangularFuzzyProbability(const double a, const double b1, const double b2, const double c, const unsigned int missionTime)
{
	Probability p(probabilitytype::TRIANGULARFUZZY);
	p.m_a = a;
	p.m_b1 = b1;
	p.m_b2 = b2;
	p.m_c = c;
	p.m_missionTime = missionTime;
	return p;
}

Probability::Probability(const probabilitytype type)
: m_type(type)
{}

NumericInterval Probability::getAlphaCutBounds(const double alpha) const
{
	switch (m_type)
	{
	case STATIC:
	case RATE:
		{
				 return NumericInterval(m_staticValue, m_staticValue);
		}
	case TRIANGULARFUZZY:
		{
			const interval_t lowerBound = alpha * (m_b1 - m_a) + m_a;
			const interval_t upperBound = m_c - alpha * (m_c - m_b2);

			return NumericInterval(lowerBound, upperBound);
		}
	case DECOMPOSEDFUZZY:
		{
			if (m_decomposedValues.find(alpha) != m_decomposedValues.end())
			return m_decomposedValues.at(alpha);

			// Alpha-cut needs to be approximated
			interval_t lowerAlpha = 0.0;
			interval_t upperAlpha = 1.0;

			// Search the biggest "lowerAlpha" and the lowest "upperAlpha"
			// such that lowerAlpha < alpha < upperAlpha 
			for (const auto& pair : m_decomposedValues)
			{
				const double a = pair.first;
				if (a < alpha && a > lowerAlpha)
					lowerAlpha = a;
				else if (a > alpha && a < upperAlpha)
					upperAlpha = a;
			}

			const NumericInterval lowerInterval = m_decomposedValues.at(lowerAlpha);
			const NumericInterval upperInterval = m_decomposedValues.at(upperAlpha);

			const interval_t lowerBound = 
				lowerInterval.lowerBound + (alpha - lowerAlpha) * 
				(upperInterval.lowerBound- lowerInterval.lowerBound);

			const interval_t upperBound = 
				upperInterval.upperBound + (upperAlpha - alpha) * 
				(lowerInterval.upperBound - upperInterval.upperBound);

			return NumericInterval(lowerBound, upperBound);
		}
	}
	assert(false && "Unexpected probability type");
	return NumericInterval(-1,-1);
}


