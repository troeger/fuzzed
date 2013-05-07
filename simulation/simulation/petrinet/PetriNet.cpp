#include "PetriNet.h"
#include "util.h"

PetriNet::PetriNet(
	const vector<ImmediateTransition>& immediateTransitions, 
	const vector<TimedTransition>& timedTransitions, 
	const map<string, Place>& places,
	const ArcList& arcDict) :
	m_immediateTransitions(immediateTransitions),
	m_timedTransitions(timedTransitions),
	m_placeDict(places),
	m_arcs(arcDict),
	m_finalFiringTime(MAX_INT)
{
	setup();
}

PetriNet::PetriNet(const PetriNet& otherNet) :
	m_immediateTransitions(otherNet.m_immediateTransitions),
	m_activeTimedTransitions(TransitionTimeMapping()),
	m_inactiveTimedTransitions(set<TimedTransition*>()),
	m_timedTransitions(otherNet.m_timedTransitions),
	m_placeDict(otherNet.m_placeDict),
	m_arcs(otherNet.m_arcs),
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
	while (!m_topLevelPlace && it != m_placeDict.end())
	{
		if (it->second.isTopLevelPlace())
			m_topLevelPlace = &it->second;
		++it;
	}
	assert(m_topLevelPlace && "the petri net must have a top level place, or the simulation won't terminate");

	int sumFiringTimes = 0;
	for (TimedTransition& tt : m_timedTransitions)
	{
		// compute random firing times for all transitions
		const int time = m_generator.randomFiringTime(tt.getRate());
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
{
	// TODO
}

PetriNet& PetriNet::operator=(const PetriNet& otherNet)
{
	m_immediateTransitions	= otherNet.m_immediateTransitions;
	m_timedTransitions		= otherNet.m_timedTransitions;
	m_placeDict				= otherNet.m_placeDict;
	m_arcs					= otherNet.m_arcs;

	setup();

	return *this;
}

int PetriNet::nextFiringTime(int currentTime)
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
	const int updatedTime = tt->getFiringTime();
	m_activeTimedTransitions.insert(make_pair(updatedTime, tt));
	
	if (updatedTime > m_finalFiringTime)
		m_finalFiringTime = updatedTime;
}