#pragma once

#include "faulttree.h"
#include "fuzztree.h"

namespace treeHelpers
{
	faulttree::BasicEvent	copyBasicEvent(const fuzztree::BasicEvent& be);
	faulttree::TopEvent		copyTopEvent(const fuzztree::TopEvent& topEvent);

	void printTree(const faulttree::Node& node, int indent);
	void printTree(const fuzztree::Node& node, int indent);

	std::string toString(const int& d);
	std::string toString(const double& d, const int& prec /*= 5*/);
	
	void replaceStringInPlace(std::string& subject, const std::string& search, const std::string& replacement);
}