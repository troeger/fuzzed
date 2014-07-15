#pragma once
#include "AbstractModel.h"
#include "FuzzTreeConfiguration.h"

class Fuzztree : public AbstractModel
{
public:
	std::vector<FuzzTreeConfiguration> generateConfigurations() const;
	Fuzztree generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration);

protected:
	void initFromGraphML(const std::string& graphMLFileName) override;

	unsigned int m_decompositionNumber;
};