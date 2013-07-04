#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"

#include "faulttree.h"
#include "FaultTreeTypes.h"

using std::string;
using std::auto_ptr;

std::auto_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree)
{
	auto_ptr<TopLevelEvent> top(new TopLevelEvent(generatedTree.id()));
	convertFaultTreeRecursive(top.get(), generatedTree);
	return top;
}

void convertFaultTreeRecursive(FaultTreeNode* node, const faulttree::Node& templateNode)
{
	using namespace faultTreeType;

	FaultTreeNode* current = nullptr;

	for (const auto& child : templateNode.children())
	{
		const string id = child.id();
		const string typeName = typeid(child).name();

		// Leaf nodes...
		if (typeName == BASICEVENT) 
		{
			const auto& prob = (static_cast<const faulttree::BasicEvent&>(child)).probability();
			const string probName = typeid(prob).name();
			assert(probName == CRISPPROB);

			float failureRate = static_cast<const faulttree::CrispProbability&>(prob).value();

			current = new BasicEvent(id, failureRate);
			node->addChild(current);
			continue;
		}
		else if (typeName == HOUSEEVENT)
		{
			current = new BasicEvent(id, 0);
			node->addChild(current);
			continue;
		}
		else if (typeName == UNDEVELOPEDEVENT)
		{
			throw std::runtime_error("Cannot simulate trees with undeveloped events!");
			continue;
		}
		else if (typeName == INTERMEDIATEEVENT)
		{
			// TODO
		}

		//  Gates...
		else if (typeName == AND)				current = new ANDGate(id);
		else if (typeName == OR)				current = new ORGate(id);
		else if (typeName == XOR)				current = new XORGate(id);
		else if (typeName == VOTINGOR)			current = new VotingORGate(id, static_cast<const faulttree::VotingOr&>(child).k());
		
		// TODO: dynamic gates...
		// else if (typeName == FDEP) current = new FDEPGate();

		node->addChild(current);
		convertFaultTreeRecursive(current, child);
	}
}
