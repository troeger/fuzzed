#pragma once
#include "PNDocument.h"
#include "Condition.h"

class TimeNETDocument : public PNDocument
{
public:
	TimeNETDocument();
	TimeNETDocument(const string& fileName);

	virtual int addTimedTransition(long double rate, const Condition& cond = Condition(), const string& label = "") override;
	virtual int addImmediateTransition(long double weight = 1.0, const Condition& cond = Condition(), const string& label = "") override;
	virtual int addTopLevelPlace(const string& label) override;

	virtual int addPlace(int initialMarking, int capacity = 1,  const string& label = "", bool isBasicEvent = false) override;
	
	virtual void addFailureMeasure() override;
	
protected:
	virtual void initXML() override;
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const string& inscription = "x") override;

	// helpers
	static void setID(xml_node& node, const int id, const NodeType type);
	static void setType(xml_node& node, const string& type="node");
	static void setLabel(xml_node& node, const string& label);
	static void setPosition(xml_node& node, const int x, const int y);

	void setTransitionProperties(xml_node &node, const string& str);

	void setHeaderTimeNET();

	// TimeNET wants the XML nodes ordered by type, so here goes...
	xml_node m_firstArc;
	xml_node m_firstTimedTransition;
	xml_node m_firstImmediateTransition;
	xml_node m_firstPlace;

	vector<string> m_basicEventLabels;

	int m_timedTransitionCount;
	int m_immediateTransitionCount;
	
	int m_lastX;
	int m_lastY;
};