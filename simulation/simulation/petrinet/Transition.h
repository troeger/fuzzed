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

	bool isActive() const { return m_active; };
	std::string getID() const { return m_ID; };
	
	void tryToFire();
	void fire(int tick);

protected:
	Transition(const std::string& id);
	
	virtual bool stochasticallyEnabled(int tick) const = 0;

	PlaceTokenMap m_inPlaces;
	PlaceTokenMap m_outPlaces;

	std::string m_ID;

	bool m_active;
	bool m_bLoggingActive;

	// true if the in-places hold enough tokens.
	// this is important because the stochastic distribution starts only at the time the transition is enabled.
	// TODO: can this be modeled with m_active? 
	// -> maybe not, because inactive transitions are never considered during simulation
	bool m_enabled;

	// the first time all in-places hold enough tokens.
	int m_startupTime;

	std::ofstream* m_log;
};