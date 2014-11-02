#include "FuzzTreeConfiguration.h"
#include "xmlutil.h"

FuzzTreeConfiguration::FuzzTreeConfiguration(const unsigned int id)
	: m_costs(0),
	m_bValid(true),
	m_id(std::to_string(id))
{
	std::cout << m_id;
}

FuzzTreeConfiguration::FuzzTreeConfiguration(const FuzzTreeConfiguration& other)
	: m_notIncluded(other.m_notIncluded),
	m_featureNodes(other.m_featureNodes),
	m_redundancyNodes(other.m_redundancyNodes),
	m_optionalNodes(other.m_optionalNodes),
	m_costs(other.m_costs),
	m_bValid(true),
	m_id(other.getId())
{
	std::cout << m_id;
}

void FuzzTreeConfiguration::operator=(const FuzzTreeConfiguration &other)
{
	m_notIncluded = other.m_notIncluded;
	m_featureNodes = other.m_featureNodes;
	m_redundancyNodes = other.m_redundancyNodes;
	m_optionalNodes = other.m_optionalNodes;
	m_costs = other.m_costs;
	m_bValid = true;
	m_id = other.getId();
	std::cout << m_id;
}


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

void FuzzTreeConfiguration::setNotIncludedRecursive(const Node& node)
{
	for (const auto child : node.getChildren())
		setNotIncludedRecursive(child);
	
	m_notIncluded.insert(node.getId());
}

const bool& FuzzTreeConfiguration::isOptionalEnabled(const id_type& ID) const
{
	assert(m_optionalNodes.find(ID) != m_optionalNodes.end());
	return m_optionalNodes.at(ID);
}

const bool FuzzTreeConfiguration::isIncluded(const id_type& ID) const
{
	return m_notIncluded.find(ID) == m_notIncluded.end();
}

const std::tuple<int,int>& FuzzTreeConfiguration::getRedundancyCount(const id_type& ID) const
{
	assert(m_redundancyNodes.find(ID) != m_redundancyNodes.end());
	return m_redundancyNodes.at(ID);
}

const FuzzTreeConfiguration::id_type& FuzzTreeConfiguration::getFeaturedChild(const id_type& ID) const
{
	assert(m_featureNodes.find(ID) != m_featureNodes.end());
	return m_featureNodes.at(ID);
}

void FuzzTreeConfiguration::setCost(unsigned int cost)
{
	m_costs = cost;
}

const unsigned int FuzzTreeConfiguration::getCost() const
{
	return m_costs;
}

const FuzzTreeConfiguration::id_type& FuzzTreeConfiguration::getId() const
{
	return m_id;
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

void FuzzTreeConfiguration::markInvalid()
{
	m_bValid = false;
}

const unsigned int FuzzTreeConfiguration::computeCostRecursive(const Node& node)
{
	unsigned int result = 0;
	if (node.canHaveCost())
		result = node.getCost();
	
	for (const auto child : node.getChildren())
		result += computeCostRecursive(child);

	return result;
}

void FuzzTreeConfiguration::setId(const unsigned int id)
{
	m_id = std::to_string(id);
}

const bool FuzzTreeConfiguration::isValid() const
{
	return m_bValid;
}
