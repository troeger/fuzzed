#pragma once
#include "Gate.h"

class ORGate : public Gate
{
public:
	ORGate(int id, const std::string& name = "");
	virtual ~ORGate(void);

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
};