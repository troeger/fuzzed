#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"

#include "faulttree.h"
#include "FaultTreeTypes.h"

using std::string;
using std::shared_ptr;

std::shared_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree)
{
	shared_ptr<TopLevelEvent> top(new TopLevelEvent(generatedTree.id()));
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
			
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == HOUSEEVENT)
		{ // TODO find out if this is legitimate
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

		// Static Gates...
		else if (typeName == AND)				current = new ANDGate(id);
		else if (typeName == OR)				current = new ORGate(id);
		else if (typeName == XOR)				current = new XORGate(id);
		else if (typeName == VOTINGOR)			current = new VotingORGate(id, static_cast<const faulttree::VotingOr&>(child).k());
		
		// Dynamic gates...
		else if (typeName == FDEP)
		{
			const faulttree::FDEP& fdep = static_cast<const faulttree::FDEP&>(child);
			const string trigger = fdep.trigger();
			std::vector<string> dependentEvents;
			for (const string& e : fdep.triggeredEvents())
				dependentEvents.emplace_back(e);
			current = new FDEPGate(id, trigger, dependentEvents);
		}
		else if (typeName == PAND)
		{
			const faulttree::PriorityAnd& pand = static_cast<const faulttree::PriorityAnd&>(child);
			std::vector<string> eventSequence;
			for (const string& e : pand.eventSequence())
				eventSequence.emplace_back(e);
			current = new PANDGate(id, eventSequence); 
		}
		else if (typeName == SEQ)
		{
			const faulttree::Sequence& seq = static_cast<const faulttree::Sequence&>(child);
			std::vector<string> eventSequence;
			for (const string& e : seq.eventSequence())
				eventSequence.emplace_back(e);
			current = new SEQGate(id, eventSequence); 
		}
		else if (typeName == SPARE)
		{
			const faulttree::Spare& spareGate = static_cast<const faulttree::Spare&>(child);
			current = new SpareGate(id, spareGate.primaryID(), spareGate.dormancyFactor()); 
		}

		if (current)
		{
			node->addChild(current);
			convertFaultTreeRecursive(current, child);
		}
		else
		{
			convertFaultTreeRecursive(node, child);
		}
	}
}
