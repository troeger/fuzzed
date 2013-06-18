#include "TNDocument.h"
#include "util.h"
#include "Constants.h"

#include <boost/format.hpp>

using std::string;

namespace
{
	const string HEADERTEMPLATE = "NET_TYPE: eDSPN\n"
		"DESCRIPTION: generated TN for fault tree simulation\n" 
		"PLACES: %1%\n"
		"TRANSITIONS: %2%\n"
		"DELAY_PARAMETERS: 0\n"
		"MARKING_PARAMETERS: 0\n"
		"REWARD_MEASURES: %3%\n\n";

	// 1: PLACES
	// 2: TRANSITIONS
	// 3: MEASURES
	const string CONTENTTEMLPATE = ""
		"-- LIST OF PLACES:\n%1%\n\n"
		"-- LIST OF TRANSITIONS:\n%2%\n\n"
		"-- LIST OF MEASURES:\n%3%\n\n";

	// NAME, MARKING, (X,Y)-POSITION (PLACE & TAG)
	// 1: NAME
	// 2: MARKING
	const string PLACETEMPLATE = "PLACE %1% %2% 0 0 0 0\n";

	//NAME, DELAY, ENABLING DEPENDENCE, KIND, FIRING POLICY, PRIORITY,ORIENTATION, PHASE, GROUP, GROUP_WEIGHT, (X,Y)-POSITION (TRANSITION, TAG & DELAY), ARCS
	// 1: NAME
	// 2: DELAY (EXPONENTIAL)
	// 3: PRIORITY
	// 4: #INPARCS
	// 6: #OUTARCS
	const string EXPTRANSITIONTEMPLATE = "TRANSITION %1% %2% IS EXP RE %3% 0 1 0 1.000000 0 0 0 0 0 0\n";
	//	"INPARCS %4% \n %5%"
	//	"OUTPARCS %6% \n %7%";

	const string IMMEDIATETRANSITIONTEMPLATE = "TRANSITION %1% %2% IS IM RE %3% 0 1 0 1.000000 0 0 0 0 0 0\n";
	//	"INPARCS %4% \n %5%"
	//	"OUTPARCS %6% \n %7%";

	const string MEASURETEMPLATE = "MEASURE %1%\n %2%\n";
}

TNDocument::TNDocument()
	: PNDocument()
{}

int TNDocument::addTimedTransition(long double rate, const std::string& /*= ""*/)
{
	const string id = TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size());
	m_transitions[id] = TN_TransitionSpec((boost::format(EXPTRANSITIONTEMPLATE) % id % (1.0/rate) % 1).str());

	return m_transitions.size()-1;
}

int TNDocument::addImmediateTransition(const unsigned int priority /*= 1*/, const std::string& /*= ""*/)
{
	const string id = TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size());
	m_transitions[id] = TN_TransitionSpec((boost::format(IMMEDIATETRANSITIONTEMPLATE) % id % 0 % priority).str());

	return m_transitions.size()-1;
}


int TNDocument::addPlace(
	int initialMarking,
	int capacity /*= 1*/,
	const std::string& /*= ""*/,
	PlaceSemantics semantics /*= DEFAULT_PLACE*/)
{
	const string id = PLACE_IDENTIFIER + util::toString((int)m_places.size());
	m_places[id] = (boost::format(PLACETEMPLATE) % id % initialMarking).str();

	return m_places.size()-1;
}

bool TNDocument::save(const string& fileName)
{
	std::ofstream file = std::ofstream(fileName, ios::binary);
	if (!file)
		return false;

	file << boost::format(HEADERTEMPLATE) % m_places.size() % m_transitions.size() % m_measures.size();

	string places;
	for (const auto& p : m_places)
		places += p.second;

 	string transitions;
	for (const auto& t : m_transitions)
		transitions += transitionString(t.second);

 	string measures;
	for (const auto& m : m_measures)
		measures += m;

	file << boost::format(CONTENTTEMLPATE) % places % transitions % measures << std::endl;
	file.close();

	return true;
}

void TNDocument::addArc(
	int placeID, int transitionID, int tokenCount, 
	ArcDirection direction, const std::string&)
{
	const string trans = transitionIdentifier(transitionID);
	
	auto it = m_transitions.find(trans);
	if (it == m_transitions.end()) return; // TODO throw?

	const string arc = util::toString(tokenCount) + " " + placeIdentifier(placeID) + " " + util::toString(0) + "\n";
	if (direction == TRANSITION_TO_PLACE)
		it->second.outputArcs.emplace_back(arc);
	else if (direction == PLACE_TO_TRANSITION)
		it->second.inputArcs.emplace_back(arc);

}

int TNDocument::addTopLevelPlace(const std::string&)
{
	const string id = PLACE_IDENTIFIER + util::toString((int)m_places.size());
	m_places[id] = (boost::format(PLACETEMPLATE) % id % 0).str();

	const string measure = (boost::format(MEASURETEMPLATE) % "SystemFailure" % (string("P{#") + id + " > 0};")).str();
	m_measures.emplace_back(measure);

	return m_places.size()-1;
}

TNDocument::~TNDocument()
{
	if (!m_bSaved)
		cout << "File was not saved" << endl;
}

const string TNDocument::transitionString(const TN_TransitionSpec& spec)
{
	string result = spec.transitionDescription;

	result += "INPARCS " + util::toString((int)spec.inputArcs.size()) + " \n";
	for (const auto& s : spec.inputArcs)
		result += s;

	result += "OUTPARCS " + util::toString((int)spec.outputArcs.size()) + "\n";
	for (const auto& s : spec.outputArcs)
		result += s;
	 
	result += "INHARCS " + util::toString((int)spec.inhibitArcs.size()) + " \n";
	for (const auto& s : spec.inhibitArcs)
		result += s;

	return result + "\n";
}

const std::string TNDocument::transitionIdentifier(const int& id)
{
	return TRANSITION_IDENTIFIER + util::toString(id);
}

const std::string TNDocument::placeIdentifier(const int& id)
{
	return PLACE_IDENTIFIER + util::toString(id);
}
