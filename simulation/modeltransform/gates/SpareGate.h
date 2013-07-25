#include "DynamicGate.h"
#include <set>

class SpareGate : public DynamicGate
{
public:
	SpareGate(const std::string& id, const std::set<std::string>& spareIndices, const double& dormancyFactor, const std::string& name ="");
	
	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serializePTNet(boost::shared_ptr<PNDocument> doc) const override;
	virtual int serializeTimeNet(boost::shared_ptr<TNDocument> doc) const override;

protected:
	std::set<std::string> m_spareIndices;
	double m_dormancyFactor;
};