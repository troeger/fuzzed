#pragma once
#include "ReaderWriterQueue.h"

#include <pugixml.hpp>
#include <string>

class FuzzTreeImport;
class ReaderWriterQueue;

class FaultTreeWriter
{
public:
	FaultTreeWriter(ReaderWriterQueue* results, FuzzTreeImport* importer);
	virtual ~FaultTreeWriter();

protected:
	void writeFaultTree(FaultTreeNode* tree, const std::string& fileName);
	void writeFaultTreeNode(FaultTreeNode* ftNode, pugi::xml_node& xmlNode);

	ReaderWriterQueue* m_inputQueue;
	FuzzTreeImport* m_importer;
};