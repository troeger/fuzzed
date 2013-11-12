#pragma once
#include <memory>
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


std::shared_ptr<fuzztree::TopEvent> faultTreeToFuzzTree(const faulttree::TopEvent& fuzzTree);
void faultTreeToFuzzTreeRecursive(
	fuzztree::Node& node,
	const faulttree::Node& templateNode);