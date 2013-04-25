#pragma once
#include "Gate.h"

class XORGate : public Gate
{
public:
	XORGate(int ID, const std::string& name);
	virtual ~XORGate();
};