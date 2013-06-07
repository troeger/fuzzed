#pragma once
#include "PNDocument.h"
#include "Condition.h"

class TimeNETDocument : public PNDocument
{
public:
	TimeNETDocument();
	TimeNETDocument(const std::string& fileName);

	virtual int addTimedTransition(long double rate, const std::string& label = "") override;
	virtual int addImmediateTransition(long double weight = 1.0, const std::string& label = "") override;
	virtual int addTopLevelPlace(const std::string& label) override;

	virtual int addPlace(int initialMarking, int capacity = 1,  const std::string& label = "", bool isBasicEvent = false) override;
	
	virtual void addFailureMeasure() override;
	
protected:
	virtual void initXML() override;
	virtual void addArc(int placeID, int transitionID, int tokenCount, ArcDirection direction, const std::string& inscription = "x") override;

	// helpers
	static void setID(pugi::xml_node& node, const int id, const NodeType type);
	static void setType(pugi::xml_node& node, const std::string& type="node");
	static void setLabel(pugi::xml_node& node, const std::string& label);
	static void setPosition(pugi::xml_node& node, const int x, const int y);

	void setTransitionProperties(pugi::xml_node &node, const std::string& str);

	void setHeaderTimeNET();

	// TimeNET wants the XML nodes ordered by type, so here goes...
	pugi::xml_node m_firstArc;
	pugi::xml_node m_firstTimedTransition;
	pugi::xml_node m_firstImmediateTransition;
	pugi::xml_node m_firstPlace;

	std::vector<std::string> m_basicEventLabels;

	int m_timedTransitionCount;
	int m_immediateTransitionCount;
	
	int m_lastX;
	int m_lastY;
};