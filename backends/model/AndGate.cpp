#include "AndGate.h"
#include <cassert>

const std::string& AndGate::getTypeDescriptor() const
{
	static const std::string str = "andGate";
	return str;
}

void AndGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
