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

using namespace pugi;
using namespace std;

/************************************************************************/
/* Abstract Class for XML documents representing Petri Nets             */
/************************************************************************/
class PNDocument : public xml_document
{
public:
	PNDocument(int id = 0);
	PNDocument(const string& fileName, int id = 0);

	virtual ~PNDocument();

	// add PetriNet component to the XML document, returning IDs
	virtual int addTimedTransition(long double rate, const Condition& cond = Condition(), const string& label = "") = 0;
	virtual int addImmediateTransition(long double weight = 1.0, const Condition& cond = Condition(), const string& label = "") = 0;
	virtual int addPlace(int initialMarking, int capacity = 100 /*a big number*/,  const string& label = "", bool isBasicEvent = false) = 0;
	virtual int addTopLevelPlace(const string& label) = 0;
	
	// wrappers around addArc
	virtual void placeToTransition(int placeID, int transitionID, int consumeCount = 1, const string& inscription = "x");
	virtual void transitionToPlace(int transitionID, int placeID, int procudeCount = 1, const string& inscription = "x");
	
	// add a measure which defines the time until the TopLevelEvent is triggered
	virtual void addFailureMeasure() {}; // TimeNET
	virtual void addSequenceConstraint(const vector<int>& sequence) {}; // SEQGate
	virtual void addUserDescription(const string& description);
	
	bool save(const string& fileName);

	bool valid() const { return !xml_document::empty(); }; // TODO
	bool saved() const { return m_bSaved; };

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const string& inscription = "x") = 0;
	virtual void initXML() = 0;

	xml_node m_root;

	int m_transitionCount;
	int m_placeCount;
	int m_arcCount;

	bool m_bSaved;

	int m_id;
};