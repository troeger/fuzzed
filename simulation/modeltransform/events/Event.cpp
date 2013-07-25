#include "Event.h"
#include "Constants.h"
#include "util.h"

Event::Event(const std::string& ID, long double failureRate, const std::string& name/* = ""*/)
	: FaultTreeNode(ID, name), m_failureRate(failureRate)
{
}


Event::Event(const std::string& ID, FuzzyNumber fuzzyFailureRate)
	: FaultTreeNode(ID), m_failureRate(fuzzyFailureRate)
{
	assert(false && "not yet implemented");
}

std::string Event::serializeAsFormula(boost::shared_ptr<PNDocument> doc) const 
{
	return PLACE_IDENTIFIER + util::toString(serializePTNet(doc));
}
