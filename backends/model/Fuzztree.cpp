#include "Fuzztree.h"

void Fuzztree::handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node)
{
	assert(false && "not yet implemented");
}

const std::string& Fuzztree::getTypeDescriptor() const
{
	static const std::string str = "fuzztree";
	return str;
}

