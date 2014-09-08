#include "Faulttree.h"

void Faulttree::handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node)
{
	assert(false && "not yet implemented");
}

const std::string& Faulttree::getTypeDescriptor() const
{
	static const std::string str = "faulttree";
	return str;
}
