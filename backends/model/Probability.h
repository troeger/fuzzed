#pragma once
#include <string>
#include <map>
#include "NumericInterval.h"

enum probabilitytype
{
	STATIC = 0,
	RATE = 1,
	TRIANGULARFUZZY = 2,
	DECOMPOSEDFUZZY = 3,
	INVALID
};

typedef std::map<double, NumericInterval> DecomposedFuzzyInterval;

class Probability
{
public:
	static Probability fromDescriptionString(const std::string descriptionString, const unsigned int missionTime);

	static Probability triangularFuzzyProbability(const double a, const double b1, const double b2, const double c, const unsigned int missionTime);
	static Probability staticProbability(const double staticValue, const unsigned int missionTime);
	static Probability rateProbability(const double rateValue, const unsigned int missionTime);

	NumericInterval getAlphaCutBounds(const double alpha) const;

	Probability(const probabilitytype type);

	const double& getRateValue()				const { return m_rateValue; }
	const double& getStaticProbabilityValue()	const { return m_staticValue; }

	const bool isFuzzy() const { return m_type == DECOMPOSEDFUZZY || m_type == TRIANGULARFUZZY; }

private:
	probabilitytype m_type;

	/**
	* Non-fuzzy (Crisp) Probability
	*/
	double m_staticValue;
	unsigned int m_missionTime;

	double m_rateValue;

	/**
	* Fuzzy Probability
	*/
	double m_a;
	double m_b1;
	double m_b2;
	double m_c;

	DecomposedFuzzyInterval m_decomposedValues;
};