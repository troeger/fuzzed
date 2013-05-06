#pragma once
#include "Gate.h"
#include <set>

/************************************************************************/
/* Fail if the first child fails before the second one					*/
/* the order being defined by the insertion order in the child list		*/
/************************************************************************/

class PANDGate : public Gate
{
public:
	PANDGate(const std::string& id, const std::set<const std::string>& priorityIDs, const std::string& name = "");
	virtual ~PANDGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	std::set<const std::string> m_prioIDs;
};

