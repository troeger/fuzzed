#include "BasicEvent.h"
#include "FuzzyProbability.h"
#include "StaticProbability.h"

const std::string& BasicEvent::getTypeDescriptor() const
{
	static const std::string str = "basicEvent";
	return str;
}

void BasicEvent::setProbabilityFromXml(const pugi::xml_node& probabilityNode)
{
	m_probability = StaticProbability(atof(probabilityNode.value()));
}
