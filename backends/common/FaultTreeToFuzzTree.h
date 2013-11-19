#pragma once
#include <memory>
#include "Issue.h"

namespace faulttree
{
	class TopEvent;
	class ChildNode;
	class Node;
}

namespace fuzztree
{
	class TopEvent;
	class ChildNode;
	class Node;
}


std::shared_ptr<fuzztree::TopEvent> faultTreeToFuzzTree(const faulttree::TopEvent& fuzzTree, std::vector<Issue>& issues);
void faultTreeToFuzzTreeRecursive(
	fuzztree::Node& node,
	const faulttree::Node& templateNode,
	std::vector<Issue>& issues);