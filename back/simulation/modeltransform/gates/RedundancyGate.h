#pragma once
#include "VotingORGate.h"

using std::string;

class RedundancyGate : public VotingORGate
{
public:
	RedundancyGate(const string& id, int from, int to, int configuredN, const string& formula, const string& name);
	virtual ~RedundancyGate(void) {};

	bool isValidConfiguration() const;
	virtual bool isValid() const override;

protected:
	int m_from;
	int m_to;
	
	string m_formulaString;

	std::function<int (int)> m_formula;
};