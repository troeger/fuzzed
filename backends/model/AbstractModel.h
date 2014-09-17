#pragma once
#include <pugixml.hpp>
#include <vector>

#include "TopEvent.h"

class AbstractModel
{
public:
	AbstractModel(std::string id, TopEvent* topEvent) : m_id(id), m_topEvent(topEvent) {};
	virtual ~AbstractModel() {};
	
	AbstractModel() : m_topEvent(nullptr) {};
	
	const TopEvent* getTopEvent() const { return m_topEvent; };

	static AbstractModel* loadGraphML(const std::string graphMLFileName);
	const std::string getId();


	virtual const std::string& getTypeDescriptor() const = 0;

protected:

	virtual void initFromGraphML(const pugi::xml_document& graphMLFile);
	virtual void loadTree(const std::vector<pugi::xml_node> nodes, const std::vector<pugi::xml_node> edges);

	virtual void loadRecursive(
		const std::vector<pugi::xml_node> nodes,
		const std::vector<pugi::xml_node> edges,
		const std::string parentId,
		AbstractNode* parentModelNode);

	virtual void handleBasicEvent(const pugi::xml_node xmlnode, AbstractNode* node) = 0;

	AbstractModel(const std::string id, const std::string type) : m_id(id), m_typeDescriptor(type) {};

	std::string m_id;
	std::string m_typeDescriptor;

	TopEvent* m_topEvent;

	unsigned int m_missionTime;
};