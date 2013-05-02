#pragma once

#include "ImmediateTransition.h"
#include "TimedTransition.h"
#include "Place.h"

#include <set>
#include <map>
#include <unordered_map>

typedef tuple<string, string, int> ArcSpec;
typedef vector<ArcSpec> ArcList;
typedef multimap<int, TimedTransition*> TransitionTimeMapping;

class PetriNet
{
	friend class PetriNetSimulation; // ugh.

public:
	typedef boost::shared_ptr<PetriNet> Ptr;

	// explicit constructor, from file import
	PetriNet(
		const vector<ImmediateTransition>& immediateTransitions, 
		const vector<TimedTransition>& timedTransitions, 
		const map<string, Place>& places,
		const ArcList& arcDict);

	PetriNet(const PetriNet& otherNet);
	PetriNet& operator=(const PetriNet& rhs);

	virtual ~PetriNet();

	// returns the next time a timed transition fires and increases internal time counter
	int nextFiringTime(int currentTime);

	void updateFiringTime(TimedTransition* tt);
	
	int finalFiringTime()		const { return m_finalFiringTime; }
	int numTimedTransitions()	const { return m_activeTimedTransitions.size(); }
	double averageFiringTime()	const { return m_avgFiringTime; }

	// check if simulation can be terminated
	bool failed() const { return m_topLevelPlace->getCurrentMarking() > 0; }

	bool hasInactiveTransitions() const { return m_inactiveTimedTransitions.size() > 0; }

protected:
	// uses the information in m_arcDict to tell each transition about its in- and out-places
	void setup();

	vector<ImmediateTransition> m_immediateTransitions; 
	vector<TimedTransition> m_timedTransitions;
	
	set<TimedTransition*> m_inactiveTimedTransitions;
	TransitionTimeMapping m_activeTimedTransitions;

	map<string, Place> m_placeDict;
	Place* m_topLevelPlace; // just a pointer into m_placeDict. shouldn't leak.

	ArcList m_arcs;

	double m_avgFiringTime;

	TransitionTimeMapping::const_iterator m_previousFiringTime;
	int m_finalFiringTime;

	RandomNumberGenerator m_generator;
};