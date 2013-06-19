#include <xercesc/parsers/XercesDOMParser.hpp>
#include "FuzzTreeTransform.h"


std::vector<ft::FaultTree> FuzzTreeTransform::(const std::string& fuzzTreeXML)
{
	try
	{
		FuzzTreeTransform transform(fuzzTreeXML);
		if (!transform.loadRootNode())
		{
			cout << "Could not load FuzzTree" << endl;
			return;
		}

		vector<FuzzTreeConfiguration> configs;
		transform.generateConfigurations(configs);

		for (const auto& instanceConfiguration : configs)
		{
			transform.generateFaultTree(instanceConfiguration);
		}
	}
	catch (std::exception& e)
	{
		cout << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Error during FuzzTree Transformation" << endl;
	}
}

FuzzTreeTransform::FuzzTreeTransform(const std::string& fuzzTreeXML) :
	m_count(0)
{
	m_parser.parse(fuzzTreeXML.c_str());
	m_document = parser.getDocument();
}

FuzzTreeTransform::~FuzzTreeTransform()
{

}

bool FuzzTreeTransform::loadRootNode()
{

}

/************************************************************************/
/* Utility methods                                                      */
/************************************************************************/

bool FuzzTreeTransform::isGate(const std::string& typeDescriptor)
{
	return
		typeDescriptor == AND_GATE ||
		typeDescriptor == OR_GATE ||
		typeDescriptor == XOR_GATE ||
		typeDescriptor == VOTING_OR_GATE ||
		typeDescriptor == PAND_GATE ||
		typeDescriptor == COLD_SPARE_GATE;
}

bool FuzzTreeTransform::isLeaf(const std::string& typeDescriptor)
{
	return 
		typeDescriptor == BASIC_EVENT || 
		typeDescriptor == UNDEVELOPED_EVENT;
}

int FuzzTreeTransform::parseID(const DOMNode* node)
{

}

std::string FuzzTreeTransform::generateUniqueId(const char* oldId)
{
	string(oldId) + "." + util::toString(++m_count);
}

/************************************************************************/
/* Generating all possible configurations initially                     */
/************************************************************************/

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const
{

}

void FuzzTreeTransform::generateConfigurationsRecursive(
	const DOMNode* node, std::vector<FuzzTreeConfiguration>& configurations) const
{

}

/************************************************************************/
/* Generating fault trees from configurations                           */
/************************************************************************/

void FuzzTreeTransform::generateFaultTree(const FuzzTreeConfiguration& configuration)
{

}

void FuzzTreeTransform::generateFaultTreeRecursive(
	const DOMNode* templateNode, /*Xerces*/ 
	ft::Node* node, /*generated internal fault tree model*/ 
	const FuzzTreeConfiguration& configuration) const
{

}

void FuzzTreeTransform::removeEmptyNodes(ft::Node* node)
{

}

void FuzzTreeTransform::expandBasicEventSet(
	const DOMNode* templateNode, /*Xerces*/ 
	ft::Node* parentNode, /*generated internal fault tree model*/ 
	const int& id, const int& defaultQuantity /*= 0*/) const
{

}

std::pair<ft::Node, bool /*isLeaf*/> FuzzTreeTransform::handleFeatureVP(
	const DOMNode* templateNode, /*Xerces*/ 
	ft::Node* node, /*generated internal fault tree model*/ 
	const FuzzTreeConfiguration& configuration, const int configuredChildId) const
{

}

