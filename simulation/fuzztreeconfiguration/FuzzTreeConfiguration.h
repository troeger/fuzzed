#pragma once

#include <map>

// No tree, just a flat data structure for configuring which nodes are enabled
class FuzzTreeConfiguration
{
public:
	FuzzTreeConfiguration();
	virtual ~FuzzTreeConfiguration();

	void setNodeOptional(int ID, bool optional);
	void setRedundancyNumber(int ID, int configuredNumber);
	void setFeatureNumber(int ID, int configuredChild);

	// TODO this throws...
	bool isOptionalEnabled(int ID) const { return m_optionalNodes.at(ID); }
	int	getRedundancyCount(int ID) const { return m_redundancyNodes.at(ID); }
	int getFeaturedChild(int ID) const { return m_featureNodes.at(ID); }

protected:

	std::map<int /*ID*/, bool /*enabled*/>						m_optionalNodes;
	std::map<int /*ID*/, int /*number of enabled children*/>	m_redundancyNodes;
	std::map<int /*ID*/, int /*ID of enabled child*/>			m_featureNodes;
};