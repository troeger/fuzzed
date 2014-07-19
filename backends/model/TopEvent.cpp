#include "TopEvent.h"

const std::string& TopEvent::getTypeDescriptor()
{
	static const std::string str = "topEvent";
	return str;
}

void TopEvent::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
