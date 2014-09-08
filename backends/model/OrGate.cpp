#include "OrGate.h"
#include <cassert>

const std::string& OrGate::getTypeDescriptor() const
{
	static const std::string str = "orGate";
	return str;
}

void OrGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
