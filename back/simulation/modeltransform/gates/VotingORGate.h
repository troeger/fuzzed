#pragma once
#include "StaticGate.h"

class VotingORGate : public StaticGate
{
public:
	VotingORGate(const std::string& id, unsigned int numVotes, const std::string& name = "");
	virtual ~VotingORGate(void) {};

	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying

	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(std::shared_ptr<PNDocument> doc) const override;

	unsigned int getNumVotes() const { return m_numVotes; };

protected:
	virtual void initActivationFunc() override;

	virtual std::string description() const override;

	unsigned int m_numVotes;
};