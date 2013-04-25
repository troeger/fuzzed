#include "FuzzTreeTransform.h"
#include "Constants.h"

using namespace pugi;
using namespace std;
using namespace fuzzTree;

void FuzzTreeTransform::transformFuzzTree(const string& fileName, const string& targetDir)
{

}

void FuzzTreeTransform::loadNode(const xml_node& node)
{

}

void FuzzTreeTransform::handleBasicEventSet(xml_node &child)
{

}

void FuzzTreeTransform::handleFeatureVP(xml_node &child)
{

}

void FuzzTreeTransform::handleRedundancyVP(xml_node &child)
{

}

FuzzTreeTransform::FuzzTreeTransform(const string& fileName)
	: XMLImport(fileName)
{

}

FuzzTreeTransform::~FuzzTreeTransform()
{
}

bool FuzzTreeTransform::loadRootNode()
{
	m_rootNode = m_document.child(FUZZ_TREE);
	if (!m_rootNode)
	{
		cout << "Missing FuzzTree Node" << endl;
		return false;
	}
	return true;
}