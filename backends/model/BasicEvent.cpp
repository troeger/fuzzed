#include "BasicEvent.h"
#include "FuzzyProbability.h"
#include "StaticProbability.h"

const std::string& BasicEvent::getTypeDescriptor()
{
	static const std::string str = "basicEvent";
	return str;
}

void BasicEvent::setProbability(const pugi::xml_node& probabilityNode)
{
	m_probability = new StaticProbability(atof(probabilityNode.value()));
}
