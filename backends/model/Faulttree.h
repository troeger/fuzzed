#pragma once
#include "AbstractModel.h"

class Faulttree : public AbstractModel
{
public:
    Faulttree() : AbstractModel() {};
    Faulttree(std::string id, TopEvent* topEvent) : AbstractModel(id, topEvent) {};

	// whatever logic is faulttree-specific. MOCUS?
	const std::string& getTypeDescriptor() const override;

protected:
	void handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node) override;
};