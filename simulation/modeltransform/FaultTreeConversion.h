#pragma once
#include <memory>

namespace faulttree
{
	class TopEvent;
	class ChildNode;
	class Node;
}

class FaultTreeNode;
class TopLevelEvent;

std::shared_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree);
void convertFaultTreeRecursive(std::shared_ptr<FaultTreeNode>  node, const faulttree::Node& templateNode);