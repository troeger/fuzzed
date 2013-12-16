#include "Event.h"
#include "Constants.h"
#include "util.h"
#include <cassert>

Event::Event(const std::string& ID, double failureRate, const std::string& name/* = ""*/)
	: FaultTreeNode(ID, name), m_failureRate(failureRate)
{
}


Event::Event(const std::string& ID, FuzzyNumber fuzzyFailureRate)
	: FaultTreeNode(ID), m_failureRate(fuzzyFailureRate)
{
	assert(false && "not yet implemented");
}

std::string Event::serializeAsFormula(std::shared_ptr<PNDocument> doc) const 
{
	static const std::string gartenzaun = "#";
	return gartenzaun + PLACE_IDENTIFIER + util::toString(serializePTNet(doc)) + ">0";
}
