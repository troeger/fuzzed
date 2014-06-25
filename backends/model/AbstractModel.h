#pragma once
#include "TopEvent.h"

class AbstractModel
{
public:
	AbstractModel(const std::string graphMLFileName)
	{
		initFromGraphML(graphMLFileName);
	};

	virtual ~AbstractModel() {};
	
	const TopEvent* getTopEvent() const { return m_topEvent; };

protected:
	void initFromGraphML(const std::string& graphMLFileName) = 0;

	AbstractModel(const std::string id, const std::string type) : m_id(id), m_typeDescriptor(type) {};

	std::string m_id;
	std::string m_typeDescriptor;

	TopEvent* m_topEvent;

	unsigned int m_missionTime;
};