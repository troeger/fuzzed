#include "VotingOrGate.h"
#include <cassert>

const std::string& VotingOrGate::getTypeDescriptor() const
{
	static const std::string str = "votingOrGate";
	return str;
}

void VotingOrGate::toPetriNet(PetriNet* pn)
{
	assert(false && "not yet implemented");
}
