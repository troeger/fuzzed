#pragma once

#include <string>
#include <map>
#include <set>
#include <tuple>

// No tree, just a flat data structure for configuring which nodes are enabled
struct FuzzTreeConfiguration
{
public:
	friend class ConfigurationResultDocument;

	typedef std::string id_type;

	FuzzTreeConfiguration();
	~FuzzTreeConfiguration();

	void setNodeOptional(const id_type& ID, bool optional);
	void setRedundancyNumber(const id_type& ID, int k, int outOfN);
	void setFeatureNumber(const id_type& ID, const id_type& configuredChild);

	void setNotIncluded(const id_type& ID);

	const bool& isOptionalEnabled(const id_type& ID)	const { return m_optionalNodes.at(ID); }
	const bool isIncluded(const id_type& ID)			const { return m_notIncluded.find(ID) == m_notIncluded.end(); }
	
	const std::tuple<int,int>& getRedundancyCount(const id_type& ID)const { return m_redundancyNodes.at(ID); }
	const id_type& getFeaturedChild(const id_type& ID)				const { return m_featureNodes.at(ID); }

protected:
	std::set<id_type>										m_notIncluded;
	std::map<id_type, bool /*enabled*/>						m_optionalNodes;
	std::map<id_type, std::tuple<int,int> /*n out of m*/>	m_redundancyNodes;
	std::map<id_type, id_type>								m_featureNodes;
};