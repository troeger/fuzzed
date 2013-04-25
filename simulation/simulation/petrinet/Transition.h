#pragma once
#include <set>
#include <boost/shared_ptr.hpp>
#include <fstream>
#include "implementation/Random.h"

class Place;

typedef std::map<Place*, int> Places;

class Transition
{
public:
	void setLogFile(std::ofstream* file);

	void setInPlaces(const Places inPlaces)		{ m_inPlaces = inPlaces; };
	void setOutPlaces(const Places outPlaces)	{ m_outPlaces = outPlaces; };

	bool wantsToFire(int tick);

	bool isActive() const { return m_active; };
	std::string getID() const { return m_ID; };
	
	void tryToFire();
	void fire(int tick);

protected:
	Transition(const std::string& id);
	
	virtual bool stochasticallyEnabled(int tick) = 0;

	Places m_inPlaces;
	Places m_outPlaces;

	std::string m_ID;

	bool m_active;
	bool m_bLoggingActive;

	std::ofstream* m_log;
};