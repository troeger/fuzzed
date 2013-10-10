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

class FaultTreeNode;
class TopLevelEvent;

std::shared_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree);
void convertFaultTreeRecursive(std::shared_ptr<FaultTreeNode> node, const faulttree::Node& templateNode, const unsigned int& missionTime);

std::shared_ptr<TopLevelEvent> fromGeneratedFuzzTree(const fuzztree::TopEvent& generatedTree);
void convertFuzzTreeRecursive(std::shared_ptr<FaultTreeNode> node, const fuzztree::Node& templateNode, const unsigned int& missionTime);