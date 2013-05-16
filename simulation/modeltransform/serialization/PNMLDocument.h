#pragma once
#include "PNDocument.h"

class PNMLDocument : public PNDocument
{
public:
	PNMLDocument();
	PNMLDocument(const string& fileName);

	virtual ~PNMLDocument();

	virtual int addTimedTransition(long double rate, const Condition& cond = Condition(), const string& label = "") override;
	virtual int addImmediateTransition(long double weight = 1.0, const Condition& cond = Condition(), const string& label = "") override;

	virtual int addPlace(int initialMarking, int capacity = 1,  const string& label = "", bool isBasicEvent = false) override;
	virtual int addTopLevelPlace(const string& label) override;
	
	virtual void addSequenceConstraint(const vector<int>& sequence) override;

protected:
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const string& inscription = "x") override;
	int addTransition(long double rate, const Condition& cond, bool isTimed, const string& label = "");
	
	// helpers
	static void setName(xml_node& node, const string& label);
	// adds a child node: <value>val</value>
	static void setNodeValue(xml_node& name, const string& val);

	virtual void initXML() override;
};