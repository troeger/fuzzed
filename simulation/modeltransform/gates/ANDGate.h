#pragma once
#include "Gate.h"

class ANDGate : public Gate
{
public:
	ANDGate(int id, const std::string& name = "");
	virtual ~ANDGate(void);

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
};

