#include "PetriNet.h"
#include "util.h"

PetriNet::PetriNet(
	const vector<ImmediateTransition>& immediateTransitions, 
	const TransitionTimeMapping& timedTransitions, 
	const map<string, Place>& places,
	const ArcList& arcDict) :
	m_immediateTransitions(immediateTransitions),
	m_timedTransitions(timedTransitions),
	m_placeDict(places),
	m_arcDict(arcDict),
	m_finalFiringTime(MAX_INT)
{
	setupConnections();
}

PetriNet::PetriNet(const PetriNet& otherNet) :
	m_immediateTransitions(otherNet.m_immediateTransitions),
	m_timedTransitions(TransitionTimeMapping()),
	m_placeDict(otherNet.m_placeDict),
	m_arcDict(otherNet.m_arcDict),
	m_finalFiringTime(MAX_INT)
{
	for (auto& p : otherNet.m_timedTransitions)
	{
		TimedTransition t(p.second);
		const int time = m_generator.randomFiringTime(t.getRate());
		t.setFiringTime(time);
		m_timedTransitions.insert(make_pair(time, t));
	}

	setupConnections();
}

void PetriNet::setupConnections()
{
	auto setPlaces = [&](Transition& t) -> void
	{
		string ID = t.getID();
		PlaceTokenMap inPlaces, outPlaces;
		for (auto& tup : m_arcDict)
		{
			const int weight = get<2>(tup);
			if (get<0>(tup) == ID) // transition-to-place
				outPlaces.insert(make_pair(&m_placeDict.at(get<1>(tup)), weight));

			else if (get<1>(tup) == ID) // place-to-transition
				inPlaces.insert(make_pair(&m_placeDict.at(get<0>(tup)), weight));
		}

		t.setInPlaces(inPlaces);
		t.setOutPlaces(outPlaces);
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
	for (auto& p : m_timedTransitions)
	{
		setPlaces(p.second);
		if (!p.second.enoughTokens())
			m_inactiveTimedTransitions.emplace(&p.second);

		sumFiringTimes += p.first;
	}

	m_avgFiringTime			= (double)sumFiringTimes/(double)m_timedTransitions.size();
	m_previousFiringTime	= m_timedTransitions.cbegin();
	m_finalFiringTime		= (--m_timedTransitions.end())->first;
}

PetriNet::~PetriNet()
{
	// TODO
}

PetriNet& PetriNet::operator=(const PetriNet& otherNet)
{
	m_immediateTransitions = otherNet.m_immediateTransitions;
	
	for (auto& p : otherNet.m_timedTransitions)
	{
		TimedTransition t(p.second);
		m_timedTransitions.insert(make_pair(t.getFiringTime(), t));
	}

	m_placeDict = otherNet.m_placeDict;
	m_arcDict = otherNet.m_arcDict;

	setupConnections();

	return *this;
}

int PetriNet::nextFiringTime(int currentTime)
{
	if (m_previousFiringTime == m_timedTransitions.cend() 
	 || m_previousFiringTime->first == m_finalFiringTime)
		return m_finalFiringTime;

	while (m_previousFiringTime->first <= currentTime)
		++m_previousFiringTime;

	return m_previousFiringTime->first;
}

void PetriNet::updateFiringTime(TimedTransition* tt, const int& updatedTime)
{
	// TODO: update the list of firing times as well as the pointer to the next time
}
