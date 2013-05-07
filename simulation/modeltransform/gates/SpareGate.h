#include "Gate.h"
#include <set>

// cold spare
class SpareGate : public Gate
{
public:
	SpareGate(const std::string& id, const std::set<std::string>& spareIndices, const std::string& name);
	virtual ~SpareGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	std::set<std::string> m_spareIndices;
};