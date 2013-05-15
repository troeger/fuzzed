#include "TimeNETDocument.h"
#include "util.h"
#include "Constants.h"
#include <assert.h>
#include <iostream>
#include <sstream>

using namespace timeNET;

int TimeNETDocument::addPlace(
	int initialMarking, 
	int capacity /*=1*/, 
	const string& label/* = ""*/, 
	bool isBasicEvent /*=false*/)
{
	assert(capacity > 0 && initialMarking >= 0);
	if (capacity < initialMarking)
	{
		cout << "WARNING: increasing capacity to " << initialMarking;
		capacity = initialMarking;
	}
	xml_node node;
	if (m_transitionCount == 0)
	{
		node = m_root.append_child(PLACE_TAG);
		m_firstPlace = node;
	}
	else
		node = m_root.insert_child_after(PLACE_TAG, m_firstPlace);

	setID(node, ++m_placeCount, PLACE);
	setPosition(node, (++m_lastX)*50, (++m_lastY)*50);

	if (initialMarking > 0)
	{
		string markingString = "";
		int i = 0;
		while (i++ < initialMarking-1)
			markingString += "true, ";
		markingString += "true";
		node.append_attribute("initialMarking").set_value(markingString.c_str());
	}

	node.append_attribute("capacity").set_value(capacity);
	node.append_attribute("queue").set_value("Random");
	node.append_attribute("tokentype").set_value("bool");
	node.append_attribute("watch").set_value(false);

	setType(node);
	const string l = label.empty() ? PLACE_IDENTIFIER+util::toString(m_placeCount) : label;
	setLabel(node,l);

	// we need these IDs for tracking which components have failed (only at the bottom level)
	// in the importance function
	if (isBasicEvent)
		m_basicEventLabels.push_back(l);

	return m_placeCount;
}

void TimeNETDocument::addArc(int placeID, int transitionID, int tokenCount, ArcDirection dir, const string& inscription /*=""*/)
{
	assert(placeID <= m_placeCount && transitionID <= m_transitionCount);

	xml_node node;
	if (m_arcCount == 0)
	{
		node = m_root.append_child(ARC_TAG);
		m_firstArc = node;
	}
	else
		node = m_root.insert_child_after(ARC_TAG, m_firstArc);

	setID(node, ++m_arcCount, ARC);
	
	string place = "p" + util::toString(placeID);
	string transition = "t" + util::toString(transitionID);
	xml_attribute sourceAttribute = node.append_attribute("fromNode");
	xml_attribute targetAttribute = node.append_attribute("toNode");

	node.append_attribute("type").set_value("connector");

	switch (dir)
	{
	case PLACE_TO_TRANSITION:
		sourceAttribute.set_value(place.c_str());
		targetAttribute.set_value(transition.c_str());
		break;
	case TRANSITION_TO_PLACE:
		sourceAttribute.set_value(transition.c_str());
		targetAttribute.set_value(place.c_str());
		break;
	default:
		assert(false);
	}

	//TODO tokenCount

	xml_node inscr = node.append_child("inscription");
	inscr.append_attribute("id").set_value(m_arcCount);
	inscr.append_attribute("text").set_value(inscription.c_str());
	inscr.append_attribute("type").set_value("inscriptionText");

	xml_node gn = inscr.append_child("graphics");
	gn.append_attribute("x").set_value("0");
	gn.append_attribute("y").set_value("0");

	assert(m_arcCount > 0);
}


TimeNETDocument::TimeNETDocument()
	: PNDocument(), 
	m_immediateTransitionCount(0),
	m_timedTransitionCount(0)
{
	initXML();
}

TimeNETDocument::TimeNETDocument(const string& fileName)
	: PNDocument(fileName),
	m_immediateTransitionCount(0),
	m_timedTransitionCount(0)
{
	initXML();
}

void TimeNETDocument::setID(xml_node& node, const int id, const NodeType type)
{
	xml_attribute idAttribute = node.append_attribute("id");
	stringstream str;
	switch (type)
	{
	case ARC:
		str << ARC_IDENTIFIER; break;
	case TRANSITION:
		str << TRANSITION_IDENTIFIER; break;
	case PLACE:
		str << PLACE_IDENTIFIER; break;
	}
	str << id;
	idAttribute.set_value(str.str().c_str());
}

void TimeNETDocument::setPosition(xml_node& node, const int x, const int y)
{
	xml_node graphicsNode = node.append_child("graphics");
	xml_attribute xa, ya;
	
	xa = graphicsNode.append_attribute("x");
	ya = graphicsNode.append_attribute("y");

	xa.set_value(x);
	ya.set_value(y);
}

void TimeNETDocument::initXML()
{
	setHeaderTimeNET();
	m_lastX = 0;
	m_lastY = 0;
}

void TimeNETDocument::setHeaderTimeNET()
{
	m_root = append_child(ROOT_TAG);

	m_root.append_attribute("xmlns").set_value("http://pdv.cs.tu-berlin.de/TimeNET/schema/SCPN");
	m_root.append_attribute("id").set_value(m_id);
	m_root.append_attribute("netclass").set_value("SCPN");
	
	m_root.append_attribute("xmlns:xsi").set_value("http://www.w3.org/2001/XMLSchema-instance");
	m_root.append_attribute("xsi:schemaLocation").set_value("http://pdv.cs.tu-berlin.de/TimeNET/schema/SCPN etc/schemas/SCPN.xsd");
}

void TimeNETDocument::setType(xml_node& node, const string& type /*="node"*/)
{
	xml_attribute typeAttr = node.append_attribute("type");
	typeAttr.set_value(type.c_str());
}

void TimeNETDocument::setLabel(xml_node& node, const string& label)
{
	xml_node labelNode = node.append_child("label");
	labelNode.append_attribute("id").set_value(label.c_str());
	labelNode.append_attribute("text").set_value(label.c_str());
	labelNode.append_attribute("type").set_value("text");
	
	xml_node labelGraphicsNode = labelNode.append_child("graphics");
	labelGraphicsNode.append_attribute("x").set_value(10);
	labelGraphicsNode.append_attribute("y").set_value(10);
}

void TimeNETDocument::addFailureMeasure()
{
	// failure if there is >= one token in top level place
	xml_node node = m_root.append_child(MEASURE_TAG);
	node.append_attribute("eval").set_value("TimeAverage");
	node.append_attribute("watch").set_value(true);
	node.append_attribute("result").set_value("fail");
	node.append_attribute("expression").set_value((string("#")+FAILURE_LABEL+">=1").c_str());
	node.append_attribute("type").set_value("text");
	node.append_attribute("id").set_value(0.1);

	xml_node graphicsNode = node.append_child("graphics");
	graphicsNode.append_attribute("x").set_value(rand()%100);
	graphicsNode.append_attribute("y").set_value(rand()%100);

	// TimeNET needs a measure called "ImportanceFunction"-
	// importance function: thresholds for RESTART simulation
	// should depend on minimal cut set length and runtime component information
	// see also http://www.eui.upm.es/sites/default/files/estudios/Tutorial%20marzo2011_villen.pdf
	xml_node importanceNode = m_root.append_child(MEASURE_TAG);
	importanceNode.append_attribute("eval").set_value("TimeAverage");
	importanceNode.append_attribute("watch").set_value(true);
	importanceNode.append_attribute("result").set_value("ImportanceFunction");
	
	importanceNode.append_attribute("type").set_value("text");
	importanceNode.append_attribute("id").set_value(0.1);

	// the number of basic events minus the number of basic events which have already occurred
	string exprString = util::toString((int)m_basicEventLabels.size()) + "- (";
	for (string& str : m_basicEventLabels)
	{
		exprString += "#" + str;
		if (str != m_basicEventLabels.back())
			exprString += "+";
		else
			exprString += ")";
	}
	importanceNode.append_attribute("expression").set_value(exprString.c_str());

	xml_node importanceGraphicsNode = importanceNode.append_child("graphics");
	importanceGraphicsNode.append_attribute("x").set_value(rand()%100);
	importanceGraphicsNode.append_attribute("y").set_value(rand()%100);
}

int TimeNETDocument::addTimedTransition(long double rate, const Condition& cond /*= Condition()*/, const string& label)
{
	assert(rate > 0.0 && "non-negative weight required");

	xml_node node;
	if (m_timedTransitionCount++ == 0)
	{ // first immediate transition.  
		m_firstTimedTransition = m_root.append_child(TIMED_TRANSITION_TAG);
		node = m_firstTimedTransition;
	}
	else
	{
		node = m_root.insert_child_before(TIMED_TRANSITION_TAG, m_firstTimedTransition);
	}
	
	if (!label.empty())
		node.append_child("label").set_value(label.c_str());

	setTransitionProperties(node, cond.asString());

	const string timeFunc = "EXP(" + util::toString(rate) + ")";
	node.append_attribute("timeFunction").set_value(timeFunc.c_str());

	return m_transitionCount;
}

int TimeNETDocument::addImmediateTransition(long double weight /*=1.0*/, const Condition& cond /*= Condition()*/, const string& label)
{
	assert(weight > 0.0 && "non-negative weight required");

	xml_node node;
	if (m_immediateTransitionCount++ == 0)
	{ // first immediate transition.
		if (m_timedTransitionCount > 0)
		{
			m_firstImmediateTransition = m_root.insert_child_after(IMMEDIATE_TRANSITION_TAG, m_firstTimedTransition);
			node = m_firstImmediateTransition;
		}
	}
	else
	{
		node = m_root.insert_child_before(IMMEDIATE_TRANSITION_TAG, m_firstImmediateTransition);
	}

	setTransitionProperties(node, cond.asString());
	node.append_attribute("weight").set_value((double)weight);
	node.append_attribute("priority").set_value((double)weight);

	if (!label.empty())
		node.append_child("label").set_value(label.c_str());

	return m_transitionCount;
}

void TimeNETDocument::setTransitionProperties(xml_node &node, const string& cond)
{
	setID(node, ++m_transitionCount, TRANSITION);

	setPosition(node, (++m_lastX)*50, (++m_lastY)*(m_lastX % 150));

	setType(node);
	setLabel(node, "T"+util::toString(m_transitionCount));
	node.append_attribute("serverType").set_value("ExclusiveServer");
	node.append_attribute("takeFirst").set_value("false");

	if (!cond.empty())
		node.append_attribute("globalGuard").set_value(cond.c_str());
}

int TimeNETDocument::addTopLevelPlace(const string& label)
{
	return addPlace(0, 1, label, false);
}
