#pragma once
#include <boost/function.hpp>
#include <map>
#include "FaultTreeNode.h"

typedef std::map<const std::string/*ID*/, long double/*value*/> NodeValueMap;

class Gate : public FaultTreeNode
{
public:
	Gate(const std::string& ID, const std::string& name);
	virtual ~Gate() {};

	virtual long double computeUnreliability() const;
	bool isDynamic() const { return m_bDynamic; };

	long double getValue() const override;

protected:
	// from all the input values, compute the value of the gate. only for static gates.
	boost::function<long double (NodeValueMap)> m_activationFunc;
	bool m_bDynamic;
};