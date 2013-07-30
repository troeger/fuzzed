#pragma once
#include "StaticGate.h"

class ORGate : public StaticGate
{
public:
	ORGate(const std::string& id, const std::string& name = "");
	virtual ~ORGate(void);

	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying

	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(std::shared_ptr<PNDocument> doc) const override;

protected:
	void initActivationFunc();
};