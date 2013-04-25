#include "FaultTreeWriter.h"
#include "FaultTreeIncludes.h"
#include "FuzzTreeImport.h"

using namespace fuzzTree;

FaultTreeWriter::FaultTreeWriter(ReaderWriterQueue* results, FuzzTreeImport* importer)
{

}

FaultTreeWriter::~FaultTreeWriter()
{
	// TODO reason about who has to tidy up
}

void FaultTreeWriter::writeFaultTree(FaultTreeNode* tree, const std::string& fileName)
{
	xml_document doc;
	
	// write header
	xml_node xmlRoot = doc.append_child(FUZZ_TREE);
	xmlRoot.append_attribute("xmlns:xsi").set_value("http://www.w3.org/2001/XMLSchema-instance");
	xmlRoot.append_attribute("xmlns:ft").set_value("de.hpi.dcl.fuzztree");

	// a well-formed fault tree has to start with a top event
	TopLevelEvent* topEvent = dynamic_cast<TopLevelEvent*>(tree);
	assert(topEvent);

	writeFaultTreeNode(topEvent, xmlRoot);

	bool bSuccess = doc.save_file(fileName.c_str());
	if (!bSuccess)
		cout << "Writing " << fileName << " failed, sorry. " << endl;
}

void FaultTreeWriter::writeFaultTreeNode(FaultTreeNode* ftNode, xml_node& xmlNode)
{

}
