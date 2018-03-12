#pragma once
#include <set>
#include <map>
#include "util.h"

class Place;

typedef std::map<Place*, unsigned int /* number of tokens consumed */> PlaceTokenMap;

/**
 * Class: Transition
 * An abstract class representing a petri net transition.
 */
class Transition
{
public:
	int nInPlaces()		const { return m_inPlaces.size(); }
	int nOutPlaces()	const { return m_outPlaces.size(); }

	/**
	 * Function: addInPlace
	 * Parameters:
	 *	p - the new input place for the transition.
	 *	numTokens - the number of tokens this transition consumes from p.
	 */
	void addInPlace(Place* p, const unsigned int& numTokens);

	/**
	 * Function: addOutPlace
	 * Parameters:
	 *	p - the new output place for the transition.
	 *	numTokens - the number of tokens this transition produces into p.
	 */
	void addOutPlace(Place* p, const unsigned int& numTokens);

	/**
	 * Function: addInhibitingPlace
	 * Parameters:
	 *	p - the new inhibiting place for the transition.
	 *	numTokens - if there are more than numTokens tokens in p, the transition will be inhibited.
	 */
	void addInhibitingPlace(Place* p, const unsigned int& numTokens);

	void removeInPlace(Place* p);
	void removeOutPlace(Place* p);

	/**
	 * Function: producesInto
	 * Returns whether the transition produces tokens into a given place.
	 */
	bool producesInto(Place* p) const { return CONTAINS(m_outPlaces, p); }

	/**
	 * Function: producesInto
	 * Returns whether the transition consumes tokens from a given place.
	 */
	bool consumesFrom(Place* p) const { return CONTAINS(m_inPlaces, p); }

	PlaceTokenMap::iterator inPlacesBegin()		{ return m_inPlaces.begin(); }
	PlaceTokenMap::iterator inPlacesEnd()		{ return m_inPlaces.end(); }
	PlaceTokenMap::iterator outPlacesBegin()	{ return m_outPlaces.begin(); }
	PlaceTokenMap::iterator outPlacesEnd()		{ return m_outPlaces.end(); }

	bool isActive() const				{ return m_hasNotFired; }
	const std::string& getID() const	{ return m_ID; }
	
	/**
	 * Function: wantsToFire
	 * Returns whether the transition could fire at time t, if it had enough tokens.
	 */
	bool wantsToFire(int tick);

	/**
	 * Function: tryToFire
	 * If this transition is both enabled and it wants to fire, try to consume tokens from all input places.
	 *
	 * See also: <Place::requestTokens>
	 */
	void tryToFire();

	/**
	 * Function: fire
	 * This transition is enabled, wants to fire, and can get enough tokens after conflict resolution.
	 * Tokens are consumed and produced in this step.
	 *
	 * See also: <Place::produceTokens>, <Place::consumeTokens>
	 */
	void fire();

	/**
	 * Function: enoughTokens
	 * Checks whether the input places contain enough tokens for this transition to fire.
	 */
	bool enoughTokens() const;

	/**
	 * Function: reset
	 * Resets the internal flags of this transition to their initial state.
	 */
	void reset();

	bool operator==(Transition const& lhs);
	Transition(const Transition& other);

protected:
	Transition(const std::string& id, const std::string& label = "");
	
	virtual bool stochasticallyEnabled(unsigned int tick) const = 0;

	PlaceTokenMap m_inPlaces;
	PlaceTokenMap m_inhibitingPlaces;
	PlaceTokenMap m_outPlaces;

	std::string m_ID;
	std::string m_label;

	bool m_hasNotFired;
	bool m_wasNotEnabled;
};