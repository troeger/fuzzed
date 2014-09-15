#pragma once

#include "ImmediateTransition.h"
#include "TimedTransition.h"
#include "Place.h"

#include <set>
#include <map>
#include <unordered_map>

enum ArcType
{
	NORMAL_ARC,
	INHIBITOR_ARC
};

typedef tuple<string, string, int, ArcType>	ArcSpec;
typedef vector<ArcSpec> ArcList;
typedef multimap<unsigned int, TimedTransition*> TransitionTimeMapping;

/**
 * Class: PetriNet
 *
 * A representation of a Generalized Stochastic Petri Net (GSPN).
 */
class PetriNet
{
	friend class PetriNetSimulation;
	friend class SequentialConstraint;

public:
	typedef std::shared_ptr<PetriNet> Ptr;

	// explicit constructor, from file import
	/**
	 * Constructor: PetriNet
	 * 
	 * Parameters:
	 * 	immediateTransitions - a list of immediate transitions, which fire at once when they are enabled.
	 *	timedTransitions - a list of timed transitions, which fire after an exponentially distributed delay.
	 *	places - a map of place identifiers to places, containing a number of tokens.
	 *	arcDict - a description of the connections between places and transitions. Each entry has the form [from id, to id, number of tokens consumed, type (normal/inhibitor)]
	 */
	PetriNet(
		const vector<ImmediateTransition>& immediateTransitions, 
		const vector<TimedTransition>& timedTransitions, 
		const map<string, Place>& places,
		const ArcList& arcDict);

	PetriNet(const PetriNet& otherNet);
	PetriNet& operator=(const PetriNet& rhs);

	virtual ~PetriNet();

	/**
	 * Function: nextFiringTime
	 * Returns the next time a timed transition fires and increases internal time counter.
	 *
	 * Parameters:
	 *	currentTime - the current discrete time tick, from which the next firing needs to be determinated.
	 */
	unsigned int nextFiringTime(const unsigned int& currentTime);

	void updateFiringTime(TimedTransition* tt);
	
	unsigned int finalFiringTime() const { return m_finalFiringTime; }
	
	unsigned int numTimedTransitions()	const { return m_timedTransitions.size(); }
	unsigned int numPlaces()			const { return m_placeDict.size(); }
	
	double averageFiringTime()	const { return m_avgFiringTime; }

	/**
	 * Function: failed
	 * Returns whether the simulation can be terminated, because the top event place contains a token (i.e., the corresponding tree has 'failed').
	 */
	bool failed() const;

	/**
	 * Function: markingInvalid
	 * Returns whether an invalid marking (due to a wrong sequence of events) was reached.
	 */
	bool markingInvalid() const;

	// 
	/**
	 * Function: hasInactiveTransitions
	 * Returns whether some immediate transitions have not yet fired, although they could be enabled (this happens when spares could yet become activated).
	 */
	bool hasInactiveTransitions() const;

	/**
	 * Function: simplify
	 * Reduces the places and immediate transitions which are not essential for the net semantics.
	 */
	void simplify();

	bool valid() const;

	/**
	 * Function: generateRandomFiringTimes
	 * Samples a random firing time for each timed transition, and saves the activated timed transitions separately. Tries to ensure that no two timed transitions have the same firing time.
	 */
	void generateRandomFiringTimes();
	
	/**
	 * Function: restoreInitialMarking
	 * Resets the entire net (all place markings and transition firing times) to its initial state. Necessary for Monte carlo simulation.
	 * 
	 * See also: <PetriNetSimulation::runOneRound>
	 */
	void restoreInitialMarking();

protected:
	/**
	 * Function: setup
	 * Uses the information in m_arcDict to tell each transition about its in- and out-places.
	 */
	void setup();

	/**
	 * Function: applyToAllTransitions
	 * Utility method for applying a lambda function to all transitions in the petri net.
	 */
	void applyToAllTransitions(std::function<void (Transition& t)> func);

	vector<ImmediateTransition> m_immediateTransitions; 
	vector<TimedTransition> m_timedTransitions;
	
	set<TimedTransition*> m_inactiveTimedTransitions;
	TransitionTimeMapping m_activeTimedTransitions;

	map<string, Place> m_placeDict;

	Place* m_topLevelPlace; // just a pointer into m_placeDict. shouldn't leak.
	vector<Place*> m_constraintPlaces;

	ArcList m_arcs;

	double m_avgFiringTime;

	TransitionTimeMapping::const_iterator m_previousFiringTime;
	unsigned int m_finalFiringTime;
};