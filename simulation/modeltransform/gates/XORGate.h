#pragma once
#include "Gate.h"

class XORGate : public Gate
{
public:
	XORGate(const std::string& ID, const std::string& name);
	virtual ~XORGate(){};

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;
};
