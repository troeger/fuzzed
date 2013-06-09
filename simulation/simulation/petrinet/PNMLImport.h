#pragma once
#include <pugixml.hpp>
#include <boost/filesystem/path.hpp>

#include "XMLImport.h"
#include "ImmediateTransition.h"
#include "TimedTransition.h"
#include "SequentialConstraint.h"
#include "Place.h"
#include "platform.h"

#include <set>
#include <map>

class PetriNet;

/************************************************************************/
/* Imports a PNML document												*/
/* generates lists of Timed/Immediate Transitions and Places from it    */
/************************************************************************/

class PNMLImport : public XMLImport
{
public:
	static PetriNet* loadPNML(const std::string& fileName) noexcept;

	virtual ~PNMLImport();

private:
	PNMLImport(const std::string& fileName);
	
	// for PetriNet.h
	void loadPlaces(std::map<std::string, Place>& placeDict);
	void loadTransitions(
		std::vector<ImmediateTransition>& immediateTransitions, 
		std::vector<TimedTransition>& timedTransitions);

	void loadArcs(std::vector<std::tuple<std::string,std::string,int>>& arcDict);

	void loadUserDescription(std::string& description);

	void loadConstraints(std::vector<SequentialConstraint>& constraints);

	virtual bool loadRootNode() override;
};
