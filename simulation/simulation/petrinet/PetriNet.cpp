#include "PetriNet.h"
#include "util.h"
#include "Constants.h"

PetriNet::PetriNet(
	const vector<ImmediateTransition>& immediateTransitions, 
	const vector<TimedTransition>& timedTransitions, 
	const map<string, Place>& places,
	const ArcList& arcDict,
	const vector<SequentialConstraint>& constraints) :
	m_immediateTransitions(immediateTransitions),
	m_timedTransitions(timedTransitions),
	m_placeDict(places),
	m_arcs(arcDict),
	m_constraints(constraints),
	m_topLevelPlace(nullptr),
	m_finalFiringTime(MAX_INT)
{
	// this is just the first petri net created from PNML import.
	// setup necessary only for its copies.
	// setup();
	// simplify();
}

PetriNet::PetriNet(const PetriNet& otherNet) :
	m_immediateTransitions(otherNet.m_immediateTransitions),
	m_activeTimedTransitions(TransitionTimeMapping()),
	m_inactiveTimedTransitions(set<TimedTransition*>()),
	m_timedTransitions(otherNet.m_timedTransitions),
	m_placeDict(otherNet.m_placeDict),
	m_arcs(otherNet.m_arcs),
	m_constraints(otherNet.m_constraints),
	m_finalFiringTime(MAX_INT)
{
	setup();
}

void PetriNet::setup()
{
	const auto setPlaces = [&](Transition& t) -> void
	{
		const string ID = t.getID();
		for (const auto& tup : m_arcs)
		{
			if (get<0>(tup) == ID) // transition-to-place
				t.addOutPlace(&m_placeDict[get<1>(tup)], get<2>(tup));

			else if (get<1>(tup) == ID) // place-to-transition
				t.addInPlace(&m_placeDict[get<0>(tup)], get<2>(tup));
		}
	};
	
	for (ImmediateTransition& t : m_immediateTransitions)
		setPlaces(t);
 
	m_topLevelPlace = nullptr;
	map<string, Place>::iterator it = m_placeDict.begin();
	const auto itEnd = m_placeDict.end();
	while (!m_topLevelPlace && it != itEnd)
	{
		if (it->second.isTopLevelPlace())
			m_topLevelPlace = &it->second;
		++it;
	}
	
	int sumFiringTimes = 0;
	RandomNumberGenerator* const gen = RandomNumberGenerator::instanceForCurrentThread();
	for (TimedTransition& tt : m_timedTransitions)
	{
		// compute random firing times for all transitions
		const unsigned int time = gen->randomFiringTime(tt.getRate());
		tt.setFiringTime(time);
		setPlaces(tt);

		// save the activated transitions separately
		if (tt.enoughTokens())
			m_activeTimedTransitions.insert(make_pair(time, &tt));
		else
			m_inactiveTimedTransitions.insert(&tt);
	}

	if (m_activeTimedTransitions.empty())
		return;

	m_avgFiringTime			= (double)sumFiringTimes/(double)m_activeTimedTransitions.size();
	m_previousFiringTime	= m_activeTimedTransitions.cbegin();
	m_finalFiringTime		= (--m_activeTimedTransitions.end())->first;
}

PetriNet::~PetriNet()
{}

PetriNet& PetriNet::operator=(const PetriNet& otherNet)
{
	m_immediateTransitions	= otherNet.m_immediateTransitions;
	m_timedTransitions		= otherNet.m_timedTransitions;
	m_placeDict				= otherNet.m_placeDict;
	m_arcs					= otherNet.m_arcs;
	m_constraints			= otherNet.m_constraints;

	m_activeTimedTransitions = TransitionTimeMapping();
	m_inactiveTimedTransitions = set<TimedTransition*>();
	m_finalFiringTime = MAX_INT;

	setup();

	return *this;
}

unsigned int PetriNet::nextFiringTime(const unsigned int& currentTime)
{
	if (m_previousFiringTime == m_activeTimedTransitions.cend() 
	 || m_previousFiringTime->first == m_finalFiringTime)
		return m_finalFiringTime;

	while (m_previousFiringTime->first <= currentTime)
		++m_previousFiringTime;

	return m_previousFiringTime->first;
}

void PetriNet::updateFiringTime(TimedTransition* tt)
{
	const unsigned int updatedTime = tt->getFiringTime();
	m_activeTimedTransitions.insert(make_pair(updatedTime, tt));
	
	if (updatedTime > m_finalFiringTime)
		m_finalFiringTime = updatedTime;
}

void PetriNet::simplify()
{ // fragments towards simplifying on the arc list??
	enum ArcEnd { BEGIN, END };

	for (ArcSpec& spec : m_arcs)
	{
		const string input = get<0>(spec);
		const string output = get<1>(spec);
		const int tokenNum = get<2>(spec);

		string transitionName, placeName;
		ArcEnd endType;
		if (util::beginsWith(input, TRANSITION_IDENTIFIER))
		{
			transitionName = input;
			placeName = output;
			endType = BEGIN;
		}
		else if (util::beginsWith(output, TRANSITION_IDENTIFIER))
		{
			transitionName = output;
			placeName = input;
			endType = END;
		}
		else continue;

		for (const ArcSpec& spec1 : m_arcs)
		{
			if (get<2>(spec1) != tokenNum) continue;

			string outputID, inputID;
			if (get<0>(spec1) == transitionName && endType == END)
			{ // place-to-transition
				outputID = get<1>(spec1);
				inputID = placeName;
			}
			else if (get<1>(spec1) == transitionName && endType == BEGIN)
			{
				outputID = placeName;
				inputID = get<0>(spec1);
			}
			else continue;
			
			assert(util::beginsWith(outputID, PLACE_IDENTIFIER) && util::beginsWith(inputID, PLACE_IDENTIFIER));
		}
	}
}


void PetriNet::applyToAllTransitions(std::function<void (Transition& t)> func)
{
	for (ImmediateTransition& it : m_immediateTransitions)
		func(it);

	for (TimedTransition& tt : m_timedTransitions)
		func(tt);
}

bool PetriNet::valid() const
{
	return m_topLevelPlace != nullptr;
}

bool PetriNet::constraintViolated()
{
	for (SequentialConstraint& c : m_constraints)
		if (!c.isSatisfied(this))
			return true;
	return false;
}