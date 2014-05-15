#pragma once

#include <string>
#include <map>
#include <set>
#include <tuple>
#include "fuzztree.h"

// No tree, just a flat data structure for configuring which nodes are enabled
struct FuzzTreeConfiguration
{
public:
	typedef std::string id_type;

	FuzzTreeConfiguration();
	FuzzTreeConfiguration(const FuzzTreeConfiguration& other);
	void operator=(const FuzzTreeConfiguration &other);
	~FuzzTreeConfiguration();

	void setOptionalEnabled(const id_type& ID, bool enabled);
	void setRedundancyNumber(const id_type& ID, int k, int outOfN);
	void setFeatureNumber(const id_type& ID, const id_type& configuredChild);

	void setNotIncludedRecursive(const fuzztree::Node& ID);

	static const int computeCostRecursive(const fuzztree::Node& ID);

	const bool& isOptionalEnabled(const id_type& ID) const;
	const bool isIncluded(const id_type& ID) const;
	
	const std::tuple<int,int>& getRedundancyCount(const id_type& ID) const;
	const id_type& getFeaturedChild(const id_type& ID) const;

	void setCost(int cost);
	const int getCost() const;

	const id_type& getId() const;

	const std::map<id_type, bool>&					getOptionalNodes() const;
	const std::map<id_type, std::tuple<int,int>>&	getRedundancyNodes() const;
	const std::map<id_type, id_type>&				getFeaturedNodes() const;

	void markInvalid();

protected:
	std::set<id_type>										m_notIncluded;
	std::map<id_type, bool /*enabled*/>						m_optionalNodes;
	std::map<id_type, std::tuple<int,int> /*n out of m*/>	m_redundancyNodes;
	std::map<id_type, id_type>								m_featureNodes;

	int m_costs;
	id_type m_id;

	bool m_bValid;
};