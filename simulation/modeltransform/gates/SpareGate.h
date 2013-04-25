#include "Gate.h"
#include <set>

using namespace std;

// cold spare
class SpareGate : public Gate
{
public:
	SpareGate(int id, const set<int>& spareIndices, const string& name);
	virtual ~SpareGate(void) {};

	virtual FaultTreeNode* clone() const override; // virtual deep copying

	virtual int serialize(boost::shared_ptr<PNDocument> doc) const override;

protected:
	set<int> m_spareIndices;
};