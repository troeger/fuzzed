#pragma once
#include "AbstractModel.h"
#include "FuzzTreeConfiguration.h"

class Fuzztree : public AbstractModel
{
public:
	std::vector<FuzzTreeConfiguration> generateConfigurations() const;
	Fuzztree* generateVariationFreeFuzzTree(const FuzzTreeConfiguration& configuration);

	const std::string& getTypeDescriptor() const override;

protected:
	void handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node) override;

	unsigned int m_decompositionNumber;
};