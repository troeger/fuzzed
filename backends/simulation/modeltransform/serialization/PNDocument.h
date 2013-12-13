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

/************************************************************************/
/* Abstract Class for XML documents representing Petri Nets             */
/************************************************************************/
class PNDocument : public pugi::xml_document
{
public:
	PNDocument(int id = 0);
	
	virtual ~PNDocument();

	// add PetriNet component to the XML document, returning IDs
	virtual int addTimedTransition(double rate, const std::string& label = "") = 0;
	virtual int addImmediateTransition(unsigned int priority = 1, const std::string& label = "") = 0;
	virtual int addPlace(int initialMarking, int capacity,  const std::string& label = "", PlaceSemantics semantics = DEFAULT_PLACE) = 0;
	virtual int addTopLevelPlace(const std::string& label) = 0;
	
	// wrappers around addArc
	virtual void placeToTransition(int placeID, int transitionID, int consumeCount = 1, const std::string& inscription = "x");
	virtual void transitionToPlace(int transitionID, int placeID, int procudeCount = 1, const std::string& inscription = "x");
	
	virtual void addInhibitorArc(int inhibitingPlace, int inhbitedTransitions, int tokenCount = 0) = 0;

	virtual void addUserDescription(const std::string& description);
	
	virtual bool save(const std::string& fileName);

	bool valid() const { return !pugi::xml_document::empty(); }
	const bool& saved() const { return m_bSaved; }

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") = 0;
	virtual void initXML() {};

	pugi::xml_node m_root;

	int m_transitionCount;
	int m_placeCount;
	int m_arcCount;

	bool m_bSaved;

	int m_id;
};
