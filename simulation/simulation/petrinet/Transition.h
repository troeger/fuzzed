#pragma once
#include <set>
#include "implementation/Random.h"
#include "util.h"

class Place;

typedef std::map<Place*, int /* number of tokens consumed */> PlaceTokenMap;

class Transition
{
public:
	int nInPlaces()		const { return m_inPlaces.size(); }
	int nOutPlaces()	const { return m_outPlaces.size(); }

	void addInPlace(Place* p, const int& numTokens);
	void addOutPlace(Place* p, const int& numTokens);

	void removeInPlace(Place* p);
	void removeOutPlace(Place* p);

	bool producesInto(Place* p) const { return CONTAINS(m_outPlaces, p); }
	bool consumesFrom(Place* p) const { return CONTAINS(m_inPlaces, p); }

	PlaceTokenMap::iterator inPlacesBegin()		{ return m_inPlaces.begin(); }
	PlaceTokenMap::iterator inPlacesEnd()		{ return m_inPlaces.end(); }
	PlaceTokenMap::iterator outPlacesBegin()	{ return m_outPlaces.begin(); }
	PlaceTokenMap::iterator outPlacesEnd()		{ return m_outPlaces.end(); }

	bool isActive() const		{ return m_hasNotFired; }
	std::string getID() const	{ return m_ID; }
	
	bool wantsToFire(int tick);
	void tryToFire();
	void fire();

	bool enoughTokens() const;

	bool operator==(Transition const& lhs);

protected:
	Transition(const std::string& id);
	
	virtual bool stochasticallyEnabled(int tick) const = 0;

	PlaceTokenMap m_inPlaces;
	PlaceTokenMap m_outPlaces;

	std::string m_ID;

	bool m_hasNotFired;
};