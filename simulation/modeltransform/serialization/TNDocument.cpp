#include "TNDocument.h"
#include "util.h"
#include "Constants.h"

#include <boost/format.hpp>

using std::string;

namespace
{
	// Some TN-WTFs
	//	- 0 transitions are not allowed (for trees with just topEvent, add a dummy transition)
	//	- the position values are NOT optional
	//	- the "comment" -- DEFINITION OF PARAMETERS: is strictly necessary and will lead to "parse error" if omitted

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
		"\n%1%\n\n"
		"\n%2%\n\n"
		"\n%3%\n\n"
		"\n%4%\n\n"
		"\n%5%\n\n"
		"\n%6%\n";

	// NAME, MARKING, (X,Y)-POSITION (PLACE & TAG)
	// 1: NAME
	// 2: MARKING
	const string PLACETEMPLATE = "PLACE %1% %2% 0.0 0.0 0.0 0.0\n";

	//NAME, DELAY, ENABLING DEPENDENCE, KIND, FIRING POLICY, PRIORITY,ORIENTATION, PHASE, GROUP, GROUP_WEIGHT, (X,Y)-POSITION (TRANSITION, TAG & DELAY), ARCS
	// 1: NAME
	// 2: DELAY (EXPONENTIAL)
	// 3: PRIORITY
	// 4: #INPARCS
	// 6: #OUTARCS
	const string EXPTRANSITIONTEMPLATE = "TRANSITION %1% %2% IS EXP RE %3% 0 1 0 1.000000 0.0 0.0 0.0 0.0 0.0 0.0\n";
	//	"INPARCS %4% \n %5%"
	//	"OUTPARCS %6% \n %7%";

	const string IMMEDIATETRANSITIONTEMPLATE = "TRANSITION %1% %2% IS IM RE %3% 0 1 0 1.000000 0.0 0.0 0.0 0.0 0.0 0.0\n";
	//	"INPARCS %4% \n %5%"
	//	"OUTPARCS %6% \n %7%";

	const string MEASURETEMPLATE = "MEASURE %1%\n%2%";

	// 1: NAME
	// 2: VALUE
	const string DEFINITIONTEMPLATE = "DELAYPAR %1% %2% 0.0 0.0";
	
	// 1: TRANSITIONID
	// 2: TERM DEPENDING ON A DEFINITION
	const string DELAYTEMPLATE = "EXP_DELAY %1% %2%;";
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


int TNDocument::addParametrisedTransition(const std::string& dependencyTerm)
{
	static const std::string MD = "<MD>";
	
	const string id = TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size());
	m_transitions[id] = TN_TransitionSpec((boost::format(EXPTRANSITIONTEMPLATE) % id % MD % 1).str());

	addParametrisedDelay(id, dependencyTerm);

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
	int /*capacity = 1*/,
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

	string definitions = "-- LIST OF DELAY PARAMETERS (NAME, VALUE, (X,Y)-POSITION):\n";
	for (const auto& d : m_definitions)
		definitions += d;

 	string transitions;
	for (const auto& t : m_transitions)
		transitions += transitionString(t.second);

	string delays = "-- MARKING DEPENDENT FIRING DELAYS FOR EXP. TRANSITIONS:\n";
	for (const auto& d : m_delays)
		delays += d;

	string enablingFunctions;
	for (const auto& f : m_enablingFunctions)
		enablingFunctions += f;

 	string measures = "\n\n"; // more than a comment...
	for (const auto& m : m_measures)
		measures += m;

	file << boost::format(CONTENTTEMLPATE) 
		% places 
		% definitions 
		% transitions 
		% delays
		% enablingFunctions
		% measures;

	file << "-- END OF SPECIFICATION FILE" << std::endl;
	file.close();

	m_bSaved = true;
	return true;
}

void TNDocument::addArc(
	int placeID, int transitionID, int tokenCount, 
	ArcDirection direction, const std::string&)
{
	const string trans = transitionIdentifier(transitionID);
	
	auto it = m_transitions.find(trans);
	if (it == m_transitions.end()) return;

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

	const string measure = (boost::format(MEASURETEMPLATE) % "S" % (string("P{#") + id + ">0};\n")).str();
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

int TNDocument::addGuardedTransition(const std::string& guard, unsigned int priority /*= 1*/)
{
	const string id = TRANSITION_IDENTIFIER + util::toString((int)m_transitions.size());
	m_transitions[id] = TN_TransitionSpec((boost::format(IMMEDIATETRANSITIONTEMPLATE) % id % 0 % priority).str());

	addEnablingFunction(id, guard);

	return m_transitions.size()-1;	
}

void TNDocument::addEnablingFunction(const std::string& transitionId, const std::string& guard)
{
	static const string functionPrefix = "FUNCTION ";
	m_enablingFunctions.emplace_back(functionPrefix + transitionId + " " + guard + ";");
}

void TNDocument::addInhibitorArc(int inhibitingPlace, int inhbitedTransition, int tokenCount /*= 0*/)
{
	const string trans = transitionIdentifier(inhbitedTransition);

	auto it = m_transitions.find(trans);
	if (it == m_transitions.end()) return;

	const string arc = util::toString(tokenCount) + " " + placeIdentifier(inhibitingPlace) + " " + util::toString(0) + "\n";
	it->second.inhibitArcs.emplace_back(arc);
}

void TNDocument::addDefinition(const std::string& name, const double& val)
{
	m_definitions.emplace_back((boost::format(DEFINITIONTEMPLATE) % name % val).str());
}

void TNDocument::addParametrisedDelay(const std::string& transitionID, const std::string& delayTerm)
{
	m_delays.emplace_back((boost::format(DELAYTEMPLATE) % transitionID % delayTerm).str());
}
