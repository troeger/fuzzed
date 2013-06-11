#pragma once

#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include "pugixml.hpp"
#include <vector>
#if IS_WINDOWS 
	#pragma warning(pop)
#endif

#include "Condition.h"
#include "petrinet/SequentialConstraint.h"

/************************************************************************/
/* Abstract Class for XML documents representing Petri Nets             */
/************************************************************************/
class PNDocument : public pugi::xml_document
{
public:
	PNDocument(int id = 0);
	PNDocument(const std::string& fileName, int id = 0);

	virtual ~PNDocument();

	// add PetriNet component to the XML document, returning IDs
	virtual int addTimedTransition(long double rate, const std::string& label = "") = 0;
	virtual int addImmediateTransition(unsigned int priority = 1, const std::string& label = "") = 0;
	virtual int addPlace(int initialMarking, int capacity,  const std::string& label = "", PlaceSemantics semantics = DEFAULT_PLACE) = 0;
	virtual int addTopLevelPlace(const std::string& label) = 0;
	
	// wrappers around addArc
	virtual void placeToTransition(int placeID, int transitionID, int consumeCount = 1, const std::string& inscription = "x");
	virtual void transitionToPlace(int transitionID, int placeID, int procudeCount = 1, const std::string& inscription = "x");
	
	// add a measure which defines the time until the TopLevelEvent is triggered
	virtual void addFailureMeasure() {}; // TimeNET
	virtual void addSequenceConstraint(const std::vector<int>&, SequenceType) {}; // SEQGate
	virtual void addUserDescription(const std::string& description);
	
	bool save(const std::string& fileName);

	bool valid() const { return !pugi::xml_document::empty(); } // TODO
	const bool& saved() const { return m_bSaved; }

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") = 0;
	virtual void initXML() = 0;

	pugi::xml_node m_root;

	int m_transitionCount;
	int m_placeCount;
	int m_arcCount;

	bool m_bSaved;

	int m_id;
};
