#pragma once
#include "Gate.h"

class VotingORGate : public Gate
{
public:
	VotingORGate(int id, int numVotes, const std::string& name = "");
	virtual ~VotingORGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

	int getNumVotes() const { return m_numVotes; };

protected:
	virtual std::string description() const override;

	int m_numVotes;
};