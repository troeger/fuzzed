#include "OrGate.h"
#include <cassert>

const std::string& XorGate::getTypeDescriptor() const
{
	static const std::string str = "xorGate";
	return str;
}

void XorGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
