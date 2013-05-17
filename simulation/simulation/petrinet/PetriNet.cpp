#include "PetriNet.h"
#include "util.h"

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
	setup();
	simplify();
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
{
	vector<ImmediateTransition> toErase;

	//   O->|->O  ==>  O
	for (ImmediateTransition& t : m_immediateTransitions)
	{
		if (t.nInPlaces() == 1 && t.nOutPlaces() == 1)
		{ // remove transition and connect all arcs to the inplace with the outplace
			Place* ip = t.inPlacesBegin()->first;
			Place* op = t.outPlacesBegin()->first;
			const int produceCount = t.outPlacesBegin()->second;
			const int consumeCount = t.inPlacesBegin()->second;
			assert(ip && op);

			if (produceCount != consumeCount) continue; // TODO: handle this case

			toErase.emplace_back(t);
			std::function<void(Transition&)> reconnect = [&](Transition& t) -> void
			{
				if (t.producesInto(ip))
				{
					t.addOutPlace(op, produceCount);
					t.removeInPlace(ip);
				}
			};

			applyToAllTransitions(reconnect);
		}
	}

	for (auto& t : toErase)
		util::removeValue(m_immediateTransitions, t);
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