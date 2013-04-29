#include "PNMLDocument.h"
#include "util.h"
#include "Constants.h"
#include <assert.h>
#include <stdexcept>

using namespace PNML;

PNMLDocument::PNMLDocument()
	: PNDocument()
{
	initXML();
}

PNMLDocument::PNMLDocument(const string& fileName)
	: PNDocument(fileName)
{
	initXML();
}

PNMLDocument::~PNMLDocument() // nothing yet
{}

int PNMLDocument::addTimedTransition(long double rate, const Condition& cond /*= Condition()*/)
{
	return addTransition(rate, cond, true);
}

int PNMLDocument::addImmediateTransition(long double weight /*= 1.0*/, const Condition& cond /*= Condition()*/)
{
	return addTransition(weight, cond, false);
}

int PNMLDocument::addPlace(
	int initialMarking, 
	int capacity /*= 1*/, 
	const string& label /*= ""*/, 
	bool isBasicEvent /*= false*/)
{	
	assert(capacity >= 0 && initialMarking >= 0 && capacity >= initialMarking);

	xml_node node;
	node = m_root.append_child(PLACE_TAG);
	const string idString = PLACE_IDENTIFIER + util::toString(++m_placeCount);
	node.append_attribute(ID_TAG).set_value(idString.c_str());
	
	setName(node, label);

	xml_node initialMarkingNode = node.append_child(INITIALMARKING_TAG);
	setNodeValue(initialMarkingNode, util::toString(initialMarking));

	xml_node capacityNode = node.append_child(CAPACITY_TAG);
	setNodeValue(capacityNode, util::toString(capacity));

	return m_placeCount;
}

void PNMLDocument::addFailureMeasure()
{
	// throw runtime_error("not yet implemented");
}

void PNMLDocument::setNodeValue(xml_node& name, const string& val)
{
	xml_node nameVal = name.append_child(VALUE_TAG);
	nameVal.append_child(node_pcdata).set_value(val.c_str());
}

void PNMLDocument::initXML()
{
	xml_node pnmlNode = append_child(PNML_TAG);
	m_root = pnmlNode.append_child(ROOT_TAG);
}

void PNMLDocument::setName(xml_node &node, const string& label)
{
	xml_node name = node.append_child(NAME_TAG);
	setNodeValue(name, label);
}

// TODO implement net-global conditions
int PNMLDocument::addTransition(long double rate, const Condition& cond, bool isTimed)
{
	xml_node transitionNode = m_root.append_child(TRANSITION_TAG);

	const string name = TRANSITION_IDENTIFIER + util::toString(++m_transitionCount);
	transitionNode.append_attribute(ID_TAG).set_value(name.c_str());
	setName(transitionNode, name);

	xml_node rateNode = transitionNode.append_child(RATE_TAG);
	setNodeValue(rateNode, util::toString(rate));

	xml_node timedNode = transitionNode.append_child(TIMED_TAG);
	setNodeValue(timedNode, isTimed ? "true":"false");

	return m_transitionCount;
}

void PNMLDocument::addArc(
	int placeID, int transitionID, int tokenCount,
	ArcDirection direction,
	const string& inscription /*= "x"*/)
{
	xml_node arcNode = m_root.append_child(ARC_TAG);
	auto arcChild = arcNode.append_child(ID_TAG);
	setNodeValue(arcChild, ARC_IDENTIFIER+util::toString(++m_arcCount));
	const string p = PLACE_IDENTIFIER+util::toString(placeID);
	const string t = TRANSITION_IDENTIFIER+util::toString(transitionID);

	switch (direction)
	{
	case PLACE_TO_TRANSITION:
		arcNode.append_attribute(SOURCE_TAG).set_value(p.c_str());
		arcNode.append_attribute(TARGET_TAG).set_value(t.c_str());
		break;
	case TRANSITION_TO_PLACE:
		arcNode.append_attribute(SOURCE_TAG).set_value(t.c_str());
		arcNode.append_attribute(TARGET_TAG).set_value(p.c_str());
		break;
	}

	auto inscrChild = arcNode.append_child(INSCRIPTION_TAG);
	setNodeValue(inscrChild, inscription+ "," + util::toString(tokenCount));

	assert(m_arcCount > 0);
}

int PNMLDocument::addTopLevelPlace(const string& label)
{
	xml_node node;
	node = m_root.append_child(PLACE_TAG);
	const string idString = PLACE_IDENTIFIER+util::toString(++m_placeCount);

	node.append_attribute(ID_TAG).set_value(idString.c_str());
	node.append_attribute(TOPLEVEL_TAG).set_value(true);

	setName(node, label+"hello");

	xml_node initialMarkingNode = node.append_child(INITIALMARKING_TAG);
	setNodeValue(initialMarkingNode, util::toString(0));

	xml_node capacityNode = node.append_child(CAPACITY_TAG);
	setNodeValue(capacityNode, util::toString(1));

	return m_placeCount;
}
