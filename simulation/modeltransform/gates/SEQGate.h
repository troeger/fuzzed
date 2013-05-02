#pragma once

#include <vector>
#include "Gate.h"

class SEQGate : public Gate
{
public:
	SEQGate(int id, const std::vector<int>& ordering, const std::string& name = "");
	virtual ~SEQGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	std::vector<int> m_ordering;
};