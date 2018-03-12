#pragma once
#include "FaultTreeNode.h"

class Gate : public FaultTreeNode
{
public:
	Gate(const std::string& ID, const std::string& name) : FaultTreeNode(ID, name) {}
	virtual ~Gate() {}
};