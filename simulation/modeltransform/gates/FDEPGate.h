#pragma once

#include "Gate.h"

class FDEPGate : public Gate
{
public:
	FDEPGate(const std::string& id, int trigger, std::vector<std::string>& dependentEvents, const std::string& name = "");
	virtual ~FDEPGate(void) {};

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	int m_triggerID;
	std::vector<std::string> m_dependentEvents;
};
