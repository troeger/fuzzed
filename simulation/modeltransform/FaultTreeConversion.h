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

std::auto_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree);
void convertFaultTreeRecursive(FaultTreeNode* node, const faulttree::Node& templateNode);