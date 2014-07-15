#pragma once
#include "AbstractModel.h"

class Faulttree : public AbstractModel
{
public:
	// whatever logic is faulttree-specific. MOCUS?

protected:
	void initFromGraphML(const std::string& graphMLFileName) override;

};