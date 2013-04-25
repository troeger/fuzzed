#pragma once
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>

#include "ImmediateTransition.h"
#include "TimedTransition.h"
#include "Place.h"

#include <set>
#include <map>
#include <unordered_map>

#include "XMLImport.h"

class PetriNet;

using namespace std;
using namespace pugi;

/************************************************************************/
/* Imports a PNML document												*/
/* generates lists of Timed/Immediate Transitions and Places from it    */
/************************************************************************/

class PNMLImport : public XMLImport
{
public:
	static PetriNet* loadPNML(const string& fileName);

	virtual ~PNMLImport();

private:
	PNMLImport(const string& fileName);
	
	// for PetriNet.h
	void loadPlaces(map<string, Place>& placeDict);
	void loadTransitions(
		vector<ImmediateTransition>& immediateTransitions, 
		multimap<int, TimedTransition>& timedTransitions);
	void loadArcs(vector<tuple<string,string,int>>& arcDict);

	void loadUserDescription(string& description);

	static int parseIntegerValue(const xml_node& node, const string& type, const int defaultValue);
	static double parseDoubleValue(const xml_node& node, const string& type, const double defaultValue);
	static bool parseBooleanValue(const xml_node& node, const string& type, const bool defaultValue);

	virtual bool loadRootNode() override;

	RandomNumberGenerator m_gen;
};