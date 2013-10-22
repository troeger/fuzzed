#include "FuzzTreeConfiguration.h"

FuzzTreeConfiguration::FuzzTreeConfiguration()
	: m_costs(0)
{}

FuzzTreeConfiguration::~FuzzTreeConfiguration()
{} // nothing

void FuzzTreeConfiguration::setOptionalEnabled(const FuzzTreeConfiguration::id_type& ID, bool enabled)
{
	m_optionalNodes[ID] = enabled;
}

void FuzzTreeConfiguration::setRedundancyNumber(const id_type& ID, int k, int outOfN)
{
	m_redundancyNodes[ID] = std::make_tuple(k, outOfN);
}

void FuzzTreeConfiguration::setFeatureNumber(const id_type& ID, const id_type& configuredChild)
{
	m_featureNodes[ID] = configuredChild;
}

void FuzzTreeConfiguration::setNotIncluded(const id_type& ID)
{
	m_notIncluded.insert(ID);
}

const bool& FuzzTreeConfiguration::isOptionalEnabled(const id_type& ID) const
{
	return m_optionalNodes.at(ID);
}

const bool FuzzTreeConfiguration::isIncluded(const id_type& ID) const
{
	return m_notIncluded.find(ID) == m_notIncluded.end();
}

const std::tuple<int,int>& FuzzTreeConfiguration::getRedundancyCount(const id_type& ID) const
{
	return m_redundancyNodes.at(ID);
}

const FuzzTreeConfiguration::id_type& FuzzTreeConfiguration::getFeaturedChild(const id_type& ID) const
{
	return m_featureNodes.at(ID);
}

void FuzzTreeConfiguration::setCost(int cost)
{
	m_costs = cost;
}

const int FuzzTreeConfiguration::getCost() const
{
	return m_costs;
}

const std::map<FuzzTreeConfiguration::id_type, bool>& FuzzTreeConfiguration::getOptionalNodes() const
{
	return m_optionalNodes;
}

const std::map<FuzzTreeConfiguration::id_type, std::tuple<int,int>>& FuzzTreeConfiguration::getRedundancyNodes() const
{
	return m_redundancyNodes;
}

const std::map<FuzzTreeConfiguration::id_type, FuzzTreeConfiguration::id_type>&
	FuzzTreeConfiguration::getFeaturedNodes() const
{
	return m_featureNodes;
}
