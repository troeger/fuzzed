#include "FuzzTreeTransform.h"
#include "FuzzTreeConfiguration.h"
#include "Constants.h"
#include "util.h"

using namespace fuzzTree;
using namespace faultTree;

using xercesc::DOMNode;
using xercesc::DOMDocument;

std::vector<faulttree::FaultTree> FuzzTreeTransform::transformFuzzTree(const std::string& fuzzTreeXML)
{
	std::vector<faulttree::FaultTree> results;
	
	try
	{
		FuzzTreeTransform transform(fuzzTreeXML);
		
		vector<FuzzTreeConfiguration> configs;
		transform.generateConfigurations(configs);

		for (const auto& instanceConfiguration : configs)
		{
			transform.generateFaultTree(instanceConfiguration);
		}
	}
	catch (xsd::cxx::exception& e)
	{
		cout << "Parse Error: " << e.what() << endl;
	}
	catch (std::exception& e)
	{
		cout << "Error during FuzzTree Transformation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Error during FuzzTree Transformation" << endl;
	}

	return results;
}

FuzzTreeTransform::FuzzTreeTransform(const std::string& fuzzTreeXML) :
	m_count(0),
	m_fuzzTree(fuzztree::fuzzTree(fuzzTreeXML.c_str()))
{
	assert(m_fuzzTree.get());
}

FuzzTreeTransform::~FuzzTreeTransform()
{}

bool FuzzTreeTransform::loadRootNode()
{
	return true;
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

std::string FuzzTreeTransform::generateUniqueId(const char* oldId)
{
	return std::string(oldId) + "." + util::toString(++m_count);
}

/************************************************************************/
/* Generating all possible configurations initially                     */
/************************************************************************/

void FuzzTreeTransform::generateConfigurations(std::vector<FuzzTreeConfiguration>& configurations) const
{

}

void FuzzTreeTransform::generateConfigurationsRecursive(
	const fuzztree::Node* node, std::vector<FuzzTreeConfiguration>& configurations) const
{

}

/************************************************************************/
/* Generating fault trees from configurations                           */
/************************************************************************/

void FuzzTreeTransform::generateFaultTree(const FuzzTreeConfiguration& configuration)
{

}

void FuzzTreeTransform::generateFaultTreeRecursive(
	const fuzztree::Node* templateNode, /*Xerces*/ 
	faulttree::Node* node, /*generated internal fault tree model*/ 
	const FuzzTreeConfiguration& configuration) const
{

}

void FuzzTreeTransform::expandBasicEventSet(
	const fuzztree::Node* templateNode,
	faulttree::Node* parentNode, 
	const int& id, const int& defaultQuantity /*= 0*/) const
{

}

std::pair<faulttree::Node, bool /*isLeaf*/> FuzzTreeTransform::handleFeatureVP(
	const fuzztree::Node* templateNode,
	faulttree::Node* node,
	const FuzzTreeConfiguration& configuration, const int configuredChildId) const
{
	assert(false && "implement");
	return make_pair(faulttree::Node(0), false);
}