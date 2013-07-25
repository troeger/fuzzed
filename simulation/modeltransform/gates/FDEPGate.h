#pragma once

#include "DynamicGate.h"

class FDEPGate : public DynamicGate
{
public:
	FDEPGate(const std::string& id, const std::string& trigger, std::vector<std::string> dependentEvents, const std::string& name = "");
	virtual ~FDEPGate(void) {};

	virtual int serializePTNet(boost::shared_ptr<PNDocument> doc) const override;
	virtual int serializeTimeNet(boost::shared_ptr<TNDocument> doc) const override;

	virtual FaultTreeNode* clone() const override; // virtual deep copying

protected:
	std::string m_triggerID;
	std::vector<std::string> m_dependentEvents;
};
