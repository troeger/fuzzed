#include "FuzzTreeConfiguration.h"

FuzzTreeConfiguration::FuzzTreeConfiguration()
{

}

FuzzTreeConfiguration::~FuzzTreeConfiguration()
{} // nothing

void FuzzTreeConfiguration::setNodeOptional(int ID, bool optional)
{
	m_optionalNodes[ID] = optional;
}

void FuzzTreeConfiguration::setRedundancyNumber(int ID, int n, int outOfM)
{
	m_redundancyNodes[ID] = std::make_tuple(n, outOfM);
}

void FuzzTreeConfiguration::setFeatureNumber(int ID, int configuredChild)
{
	m_featureNodes[ID] = configuredChild;
}

void FuzzTreeConfiguration::setNotIncluded(int ID)
{
	m_notIncluded.insert(ID);
}