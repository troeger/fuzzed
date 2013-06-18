#pragma once
#include "StaticGate.h"

class ORGate : public StaticGate
{
public:
	ORGate(const std::string& id, const std::string& name = "");
	virtual ~ORGate(void);

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const override;
};