#pragma once

#include <fstream>
#include <string>
#include "FaultTreeNode.h"

class GraphParser
{
public:
	static FaultTreeNode::Ptr fromGraphML(const std::string& fileName, std::ofstream* logfile);

private:
	GraphParser(const std::string& fileName);
	FaultTreeNode::Ptr parse();

	std::ifstream m_file;
};
