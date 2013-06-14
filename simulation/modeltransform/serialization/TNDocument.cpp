#include "TNDocument.h"
#include "util.h"
#include "Constants.h"

#include <boost/format.hpp>

using std::string;

namespace
{
	const string HEADERTEMPLATE = "NET_TYPE: eDSPN \n"
		"DESCRIPTION: generated TN for fault tree simulation \n" 
		"PLACES: %1% \n"
		"TRANSITIONS: %2% \n"
		"DELAY_PARAMETERS: 0 \n"
		"MARKING_PARAMETERS: 0 \n"
		"REWARD_MEASURES: %3%";

	// 1: PLACES
	// 2: TRANSITIONS
	// 3: MEASURES
	const string CONTENTTEMLPATE = "-- LIST OF PLACES: %1% \n"
		"-- TRANSITIONS %2% \n"
		"-- MEASURES %2%";

	// NAME, MARKING, (X,Y)-POSITION (PLACE & TAG)
	// 1: NAME
	// 2: MARKING
	const string PLACETEMPLATE = "PLACE %1% %2%";

	//NAME, DELAY, ENABLING DEPENDENCE, KIND, FIRING POLICY, PRIORITY,ORIENTATION, PHASE, GROUP, GROUP_WEIGHT, (X,Y)-POSITION (TRANSITION, TAG & DELAY), ARCS
	// 1: NAME
	// 2: DELAY (EXPONENTIAL)
	// 3: PRIORITY
	// 4: #INPARCS
	// 6: #OUTARCS
	const string EXPTRANSITIONTEMPLATE = "TRANSITION %1% %2% IS EXP RE %3% 0 1 0 1.000000"
		"INPARCS %4% \n %5%"
		"OUTPARCS %6% \n %7%";

	const string IMMEDIATETRANSITIONTEMPLATE = "TRANSITION %1% %2% IS IM RE %3% 0 1 0 1.000000"
		"INPARCS %4% \n %5%"
		"OUTPARCS %6% \n %7%";
}

TNDocument::TNDocument()
	: PNDocument()
{}

int TNDocument::addTimedTransition(long double rate, const std::string& label /*= ""*/)
{
	const string id = label.empty() ? TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size()) : label;
	m_transitions[id] = (boost::format(EXPTRANSITIONTEMPLATE) % id % (1/rate) % 1).str();

	return m_transitions.size();
}

int TNDocument::addImmediateTransition(const unsigned int priority /*= 1*/, const std::string& label /*= ""*/)
{
	const string id = label.empty() ? TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size()) : label;
	m_transitions[id] = (boost::format(IMMEDIATETRANSITIONTEMPLATE) % id % 0 % priority).str();

	return m_transitions.size();
}


int TNDocument::addPlace(
	int initialMarking,
	int capacity /*= 1*/,
	const std::string& label /*= ""*/,
	PlaceSemantics semantics /*= DEFAULT_PLACE*/)
{
	const string id = label.empty() ? PLACE_IDENTIFIER + util::toString((int)m_places.size()) : label;
	m_places[label] = (boost::format(PLACETEMPLATE) % id % initialMarking).str();

	return m_places.size();
}

bool TNDocument::save(const string& fileName)
{
	std::fstream file(fileName);
	if (!file)
		return false;

	file << boost::format(HEADERTEMPLATE) % m_places.size() % m_transitions.size() % m_measures.size();

	string places;
	for (const auto& p : m_places)
		places += p.second;

	string transitions;
	for (const auto& t : m_transitions)
		transitions += t.second;

	string measures;
	for (const auto& m : m_measures)
		measures += m;

	file << boost::format(CONTENTTEMLPATE) % places % transitions % measures;
	file.close();
}

void TNDocument::addArc(
	int placeID, int transitionID, int tokenCount, 
	ArcDirection direction, const std::string& inscription /*= "x"*/)
{
	// TODO
}

int TNDocument::addTopLevelPlace(const std::string& label)
{
	const string id = label.empty() ? PLACE_IDENTIFIER + util::toString((int)m_places.size()) : label;
	m_places[label] = (boost::format(PLACETEMPLATE) % id % 0).str();

	m_measures.emplace_back("P{#" + id + ">0};");

	return m_places.size();
}

TNDocument::~TNDocument()
{
	if (!m_bSaved)
		cout << "File was not saved" << endl;
}
