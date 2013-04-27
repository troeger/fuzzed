#include "FuzzTreeConfiguration.h"

FuzzTreeConfiguration::FuzzTreeConfiguration()
{

}

FuzzTreeConfiguration::~FuzzTreeConfiguration()
{

}

void FuzzTreeConfiguration::setNodeOptional(int ID, bool optional)
{
	m_optionalNodes[ID] = optional;
}

void FuzzTreeConfiguration::setRedundancyNumber(int ID, int configuredNumber)
{
	m_redundancyNodes[ID] = configuredNumber;
}

void FuzzTreeConfiguration::setFeatureNumber(int ID, int configuredChild)
{
	m_featureNodes[ID] = configuredChild;
}
