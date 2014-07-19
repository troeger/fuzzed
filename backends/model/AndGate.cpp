#include "AndGate.h"

const std::string& AndGate::getTypeDescriptor()
{
	static const std::string str = "andGate";
	return str;
}

void AndGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
