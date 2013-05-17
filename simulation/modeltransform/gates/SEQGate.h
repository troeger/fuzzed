#pragma once

#include <vector>
#include "Gate.h"

// TODO: think about the semantics.
// currently, simulations where the children do not occur in the right sequence are aborted.
// since the probability of the specific sequence can be low, this results in very few completed simulation rounds.

class SEQGate : public Gate
{
public:
	SEQGate(const std::string& id, const std::vector<std::string>& ordering, const std::string& name = "");
	virtual ~SEQGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	std::vector<std::string> m_ordering;
};