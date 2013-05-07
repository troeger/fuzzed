#pragma once
#include <set>
#include <unordered_map>
#include <boost/shared_ptr.hpp>
#include <fstream>
#include "implementation/Random.h"

class Place;

typedef std::map<Place*, int /* number of tokens consumed */> PlaceTokenMap;

class Transition
{
public:
	void addInPlace(Place* p, const int& numTokens);
	void addOutPlace(Place* p, const int& numTokens);

	bool isActive() const		{ return m_hasNotFired; };
	std::string getID() const	{ return m_ID; };
	
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