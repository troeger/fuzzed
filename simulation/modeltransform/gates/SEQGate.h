#pragma once

#include <vector>
#include "PANDGate.h"

// TODO: think about the semantics.
// currently, simulations where the children do not occur in the right sequence are aborted.
// since the probability of the specific sequence can be low, this results in very few completed simulation rounds.

#define STATIC_SEQUENCE 1

class SEQGate : public PANDGate
{
public:
	SEQGate(const std::string& id, const std::vector<std::string>& ordering, const std::string& name = "");
	virtual ~SEQGate(void) {};

	virtual int serializeTimeNet(boost::shared_ptr<TNDocument> doc) const override;
	virtual FaultTreeNode* clone() const override; // virtual deep copying

protected:
	virtual int addSequenceViolatedPlace(boost::shared_ptr<PNDocument> doc) const override;

	std::vector<std::string> m_ordering;
};