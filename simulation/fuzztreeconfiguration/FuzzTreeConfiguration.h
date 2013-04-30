#pragma once

#include <map>
#include <set>

// No tree, just a flat data structure for configuring which nodes are enabled
struct FuzzTreeConfiguration
{
public:
	FuzzTreeConfiguration();
	virtual ~FuzzTreeConfiguration();

	void setNodeOptional(int ID, bool optional);
	void setRedundancyNumber(int ID, int configuredNumber);
	void setFeatureNumber(int ID, int configuredChild);

	void setNotIncluded(int ID);

	// TODO this throws...
	bool isOptionalEnabled(int ID)	const { return m_optionalNodes.at(ID); }
	bool isIncluded(int ID)			const { return m_notIncluded.find(ID) == m_notIncluded.end(); }
	
	int	getRedundancyCount(int ID)	const { return m_redundancyNodes.at(ID); }
	int getFeaturedChild(int ID)	const { return m_featureNodes.at(ID); }

protected:
	std::set<int> m_notIncluded;
	std::map<int /*ID*/, bool /*enabled*/>						m_optionalNodes;
	std::map<int /*ID*/, int /*number of enabled children*/>	m_redundancyNodes;
	std::map<int /*ID*/, int /*ID of enabled child*/>			m_featureNodes;
};