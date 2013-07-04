#pragma once
#include "StaticGate.h"

class XORGate : public StaticGate
{
public:
	XORGate(const std::string& ID, const std::string& name = "");
	
	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const;

protected:
	virtual void initActivationFunc();
};