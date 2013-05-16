#pragma once
#include "Gate.h"

class XORGate : public Gate
{
public:
	XORGate(const std::string& ID, const std::string& name);
	virtual ~XORGate(){};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
};
