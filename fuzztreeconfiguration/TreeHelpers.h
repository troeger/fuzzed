#pragma once

#include "faulttree.h"
#include "fuzztree.h"

namespace treeHelpers
{
	faulttree::BasicEvent		copyBasicEvent(const fuzztree::BasicEvent& be);
	faulttree::CrispProbability	copyProbability(const fuzztree::Probability& prob);
	faulttree::TopEvent			copyTopEvent(const fuzztree::TopEvent& topEvent);

	void printTree(const faulttree::Node& node, int indent);
	void printTree(const fuzztree::Node& node, int indent);
}