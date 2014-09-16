#pragma once
#include "AbstractModel.h"
#include "FuzzTreeConfiguration.h"

class Fuzztree : public AbstractModel
{
public:
    Fuzztree() : AbstractModel() {};
    Fuzztree(std::string id, TopEvent* topEvent) : AbstractModel(id, topEvent) {};
    
	const std::string& getTypeDescriptor() const override;

protected:
	void handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node) override;

	unsigned int m_decompositionNumber;
};