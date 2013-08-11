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
	m_finalFiringTime(MAX_INT),
	m_avgFiringTime(MAX_INT)
{
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
		const string& ID = t.getID();
		for (const auto& tup : m_arcs)
		{
			if (get<0>(tup) == ID) // transition-to-place
			{
				t.addOutPlace(&m_placeDict[get<1>(tup)], get<2>(tup));
			}
			else if (get<1>(tup) == ID) // place-to-transition or inhibitor arc
			{
				if (get<3>(tup) == INHIBITOR_ARC)
					t.addInhibitingPlace(&m_placeDict[get<0>(tup)], get<2>(tup));
				else
					t.addInPlace(&m_placeDict[get<0>(tup)], get<2>(tup));
			}
		}
	};
	
	applyToAllTransitions(setPlaces);
 
	m_topLevelPlace = nullptr;
	map<string, Place>::iterator it = m_placeDict.begin();
	const auto itEnd = m_placeDict.end();
	while (!m_topLevelPlace && it != itEnd)
	{
		if (it->second.isTopLevelPlace())
		{
			assert(m_topLevelPlace == nullptr);
			m_topLevelPlace = &it->second;
		}
		else if (it->second.isConstraintPlace())
		{
			m_constraintPlaces.emplace_back(&it->second);
		}
		++it;
	}
}

PetriNet::~PetriNet()
{

}

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
	return true;//m_topLevelPlace;
}

void PetriNet::generateRandomFiringTimes()
{ // TODO factor out the things that can happen earlier
	m_activeTimedTransitions.clear();
	m_inactiveTimedTransitions.clear();

	int sumFiringTimes = 0;
	RandomNumberGenerator* const gen = RandomNumberGenerator::instanceForCurrentThread();
	for (TimedTransition& tt : m_timedTransitions)
	{
		// compute random firing times for all transitions
		const unsigned int time = gen->randomFiringTime(tt.getRate());
		tt.setFiringTime(time);

		// save the activated transitions separately
		if (tt.enoughTokens())
		{
			m_activeTimedTransitions.insert(make_pair(time, &tt));
			sumFiringTimes += time;
		}
		else
			m_inactiveTimedTransitions.insert(&tt);
	}

	if (m_activeTimedTransitions.empty())
		return;

	m_avgFiringTime			= (double)sumFiringTimes/(double)m_activeTimedTransitions.size();
	m_previousFiringTime	= m_activeTimedTransitions.cbegin();
	m_finalFiringTime		= (--m_activeTimedTransitions.end())->first;

	assert(m_activeTimedTransitions.size() + m_inactiveTimedTransitions.size() == m_timedTransitions.size());
}

void PetriNet::restoreInitialMarking()
{
	for (auto& p : m_placeDict)
		p.second.reset();

	applyToAllTransitions(std::mem_fn(&Transition::reset));
}

bool PetriNet::failed() const
{
	return m_topLevelPlace->getCurrentMarking() > 0;
}

bool PetriNet::hasInactiveTransitions() const
{
	return !m_inactiveTimedTransitions.empty();
}

bool PetriNet::markingInvalid() const
{
	for (const auto& place : m_constraintPlaces)
		if (place->getCurrentMarking() > 0) return true;

	return false;
}