#include "OrGate.h"

const std::string& OrGate::getTypeDescriptor()
{
	static const std::string str = "orGate";
	return str;
}

void OrGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
