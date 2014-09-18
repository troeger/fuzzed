#include "DynamicGate.h"
#include <set>

class SpareGate : public DynamicGate
{
public:
	SpareGate(const std::string& id, const std::string& primaryId, const double& dormancyFactor, const std::string& name ="");
	
	virtual FaultTreeNode::Ptr clone() const override; // virtual deep copying

	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const override;

protected:
	std::string m_primaryId;
	double m_dormancyFactor;
};