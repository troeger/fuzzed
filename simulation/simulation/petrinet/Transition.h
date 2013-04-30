#pragma once
#include <set>
#include <boost/shared_ptr.hpp>
#include <fstream>
#include "implementation/Random.h"

class Place;

typedef std::map<Place*, int /* number of tokens consumed */> PlaceTokenMap;

class Transition
{
public:
	void setLogFile(std::ofstream* file);

	void setInPlaces(const PlaceTokenMap inPlaces)		{ m_inPlaces = inPlaces; };
	void setOutPlaces(const PlaceTokenMap outPlaces)	{ m_outPlaces = outPlaces; };

	bool wantsToFire(int tick);

	bool isActive() const		{ return m_hasNotFired; };
	std::string getID() const	{ return m_ID; };
	
	void tryToFire();
	void fire(int tick);

	bool enoughTokens() const;

	bool operator==(Transition const& lhs);

protected:
	Transition(const std::string& id);
	virtual ~Transition();
	
	virtual bool stochasticallyEnabled(int tick) const = 0;

	PlaceTokenMap m_inPlaces;
	PlaceTokenMap m_outPlaces;

	std::string m_ID;

	bool m_hasNotFired;
	bool m_bLoggingActive;

	std::ofstream* m_log;
};