#pragma once

#include "ImmediateTransition.h"
#include "TimedTransition.h"
#include "Place.h"
#include "SequentialConstraint.h"

#include <set>
#include <map>
#include <unordered_map>

typedef tuple<string, string, int>	ArcSpec;
typedef vector<ArcSpec>				ArcList;
typedef multimap<unsigned int, TimedTransition*> TransitionTimeMapping;

class PetriNet
{
	friend class PetriNetSimulation; // ugh.
	friend class SequentialConstraint; // yikes.

public:
	typedef boost::shared_ptr<PetriNet> Ptr;

	// explicit constructor, from file import
	PetriNet(
		const vector<ImmediateTransition>& immediateTransitions, 
		const vector<TimedTransition>& timedTransitions, 
		const map<string, Place>& places,
		const ArcList& arcDict,
		const vector<SequentialConstraint>& constraints);

	PetriNet(const PetriNet& otherNet);
	PetriNet& operator=(const PetriNet& rhs);

	virtual ~PetriNet();

	// returns the next time a timed transition fires and increases internal time counter
	unsigned int nextFiringTime(const unsigned int& currentTime);

	void updateFiringTime(TimedTransition* tt);
	
	unsigned int finalFiringTime() const { return m_finalFiringTime; }
	
	unsigned int numTimedTransitions()	const { return m_activeTimedTransitions.size(); }
	unsigned int numPlaces()			const { return m_placeDict.size(); }
	
	double averageFiringTime()	const { return m_avgFiringTime; }

	// check if simulation can be terminated
	bool failed() const { return m_topLevelPlace->getCurrentMarking() > 0; }

	bool hasInactiveTransitions() const { return !m_inactiveTimedTransitions.empty(); }

	// reduce number of places and immediate transitions which are not essential for the net semantics
	void simplify();

	bool valid() const;

	bool constraintViolated();

	void generateRandomFiringTimes();
	void restoreInitialMarking();

protected:
	// uses the information in m_arcDict to tell each transition about its in- and out-places
	void setup();

	void applyToAllTransitions(std::function<void (Transition& t)> func);

	vector<SequentialConstraint> m_constraints;

	vector<ImmediateTransition> m_immediateTransitions; 
	vector<TimedTransition> m_timedTransitions;
	
	set<TimedTransition*> m_inactiveTimedTransitions;
	TransitionTimeMapping m_activeTimedTransitions;

	map<string, Place> m_placeDict;
	Place* m_topLevelPlace; // just a pointer into m_placeDict. shouldn't leak.

	ArcList m_arcs;

	double m_avgFiringTime;

	TransitionTimeMapping::const_iterator m_previousFiringTime;
	unsigned int m_finalFiringTime;
};