#pragma once
#include "StaticGate.h"

class XORGate : public StaticGate
{
public:
	XORGate(const std::string& ID, const std::string& name = "");
	
	FaultTreeNode::Ptr clone() const override; // virtual deep copying

	int serializePTNet(std::shared_ptr<PNDocument> doc) const override;
	std::string serializeAsFormula(std::shared_ptr<PNDocument> doc) const override;

protected:
	void initActivationFunc() override;
};
