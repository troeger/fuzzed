#pragma once
#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <boost/shared_ptr.hpp>
#include <set>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

/************************************************************************/
/* Conflict resolution based on:										*/ 
/* http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.110.2081		*/ 
/* "race with age memory" + atomic firing								*/
/************************************************************************/

#include "implementation/Random.h"
#include "Types.h"

class Transition;

class Place
{
public:
	typedef std::shared_ptr<Place> Ptr;

	Place(const std::string& id, int initialMarking, int capacity, PlaceSemantics semantics);
	Place(); // satisfy the compiler

	// copying
	Place(const Place& other);
	
	const std::string& getID() const { return m_ID; }
	int getCurrentMarking() const { return m_marking; }
	
	bool hasRequests() const { return !m_transitionQueue.empty(); }

	void resolveConflictsImmediate(int tick);
	void resolveConflictsTimed(int tick);

	void produceTokens(int numTokens);
	void consumeTokens(Transition* const t, int numTokens);
	void requestTokens(Transition* const t);

	const bool isTopLevelPlace() const { return m_semantics == TOP_LEVEL_PLACE; }
	const bool isConstraintPlace() const { return m_semantics ==  CONSTRAINT_VIOLATED_PLACE; }

	void reset();

protected:
	// the set of transitions who requested a token and are enabled
	std::set<Transition*> m_transitionQueue;

	int m_marking;
	const int m_initialMarking;
	
	const std::string m_ID;
	const int m_capacity;

	PlaceSemantics m_semantics;
};