#pragma once
#include "StaticGate.h"

class VotingORGate : public StaticGate
{
public:
	VotingORGate(const std::string& id, int numVotes, const std::string& name = "");
	virtual ~VotingORGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serializePTNet(boost::shared_ptr<PNDocument> doc) const override;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const override;

	int getNumVotes() const { return m_numVotes; };

protected:
	virtual void initActivationFunc() override;

	virtual std::string description() const override;

	int m_numVotes;
};