#include "FuzzTreeConfiguration.h"

FuzzTreeConfiguration::FuzzTreeConfiguration()
{

}

FuzzTreeConfiguration::~FuzzTreeConfiguration()
{} // nothing

void FuzzTreeConfiguration::setNodeOptional(const id_type& ID, bool optional)
{
	m_optionalNodes[ID] = optional;
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