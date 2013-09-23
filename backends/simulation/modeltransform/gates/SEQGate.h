#pragma once

#include <vector>
#include "PANDGate.h"

class SEQGate : public PANDGate
{
public:
	SEQGate(const std::string& id, const std::vector<std::string>& ordering, const std::string& name = "");
	virtual ~SEQGate(void) {};

	int addSequenceViolatedPlace(std::shared_ptr<PNDocument> doc) const override;
	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying
};