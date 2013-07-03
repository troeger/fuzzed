#pragma once
#include <boost/function.hpp>
#include <map>
#include "Gate.h"

typedef std::map<const std::string/*ID*/, long double/*value*/> NodeValueMap;

class StaticGate : public Gate
{
public:
	StaticGate(const std::string& ID, const std::string& name);
	virtual ~StaticGate() {}

	virtual long double computeUnreliability() const;
	bool isDynamic() const { return false; }

protected:
	virtual void initActivationFunc() = 0;

	// from all the input values, compute the value of the gate. only for static gates.
	boost::function<long double (NodeValueMap)> m_activationFunc;
};