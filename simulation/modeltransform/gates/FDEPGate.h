#pragma once

class FDEPGate : public Gate
{
public:
	FDEPGate(int id, int trigger, std::vector<int> dependentEvents, const std::string& name = "");
	virtual ~FDEPGate(void) {};

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	int m_triggerID;
};