#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include "ExpressionParser.h"
#include <algorithm>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

#include "RedundancyGate.h"
#include "util.h"

RedundancyGate::RedundancyGate(int id, int from, int to, int configuredN, const string& formula, const string& name)
	: VotingORGate(id, 0, name), 
	m_formulaString(formula), 
	m_from(from), m_to(to)
{
	assert(configuredN >= m_from && configuredN <= m_to);
	
	m_formula = [&](int n) -> int
	{
		ExpressionParser<int> parser;
		util::replaceStringInPlace(m_formulaString, "N", util::toString(n));
		return parser.eval(m_formulaString);
	};

	m_numVotes = m_formula(configuredN);
}

bool RedundancyGate::isValidConfiguration() const
{
	return 
		m_numVotes > 0 && 
		m_numVotes <= m_to && 
		m_numVotes >= m_from;
}

bool RedundancyGate::isValid() const 
{
	return isValidConfiguration() && (m_numVotes <= getNumChildren());
}
