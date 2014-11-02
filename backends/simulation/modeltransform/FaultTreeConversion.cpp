#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"

#include "util.h"
#include "xmlutil.h"
#include "FatalException.h"

using std::string;
using std::shared_ptr;
using std::make_shared;

std::shared_ptr<TopLevelEvent> fromGraphModel(const Model& m)
{
	shared_ptr<TopLevelEvent> top(new TopLevelEvent(m.getTopEvent()->getId(), m.getMissionTime()));
	convertFaultTreeRecursive(top, *(m.getTopEvent()), m.getMissionTime());
	return top;
}

void convertFaultTreeRecursive(FaultTreeNode::Ptr node, const Node& templateNode, const unsigned int& missionTime)
{
	FaultTreeNode::Ptr current = nullptr;

	for (const auto& child : templateNode.getChildren())
	{
		const string id = child.getId();
		const string typeName = child.getType();
		bool alreadyAdded = false;
		
		// Leaf nodes...
		if (typeName == nodetype::BASICEVENT) 
		{
			const Probability& prob = child.getProbability();
			
			if (prob.isFuzzy())
				throw FatalException("Cannot convert fuzzy numbers to failure rates");

			current = make_shared<BasicEvent>(id, prob.getRateValue());
			node->addChild(current);
			alreadyAdded = true;
			
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == nodetype::BASICEVENTSET)
		{
			const Probability& prob = child.getProbability();
			const unsigned int quantity = child.getQuantity();

			if (prob.isFuzzy())
				throw FatalException("Cannot convert fuzzy numbers to failure rates", 0, child.getId());

			for (int i = 0; i < quantity; ++i)
			{
				node->addChild(make_shared<BasicEvent>(id, prob.getRateValue()));
			}
			continue; // TODO these might also be triggered by FDEP
		}
		else if (typeName == nodetype::HOUSEEVENT)
		{ // TODO find out if this is legitimate
			current = make_shared<BasicEvent>(id, 0.0);
			node->addChild(current);
			continue;
		}
		else if (typeName == nodetype::UNDEVELOPEDEVENT)
		{
			throw FatalException("Cannot simulate models including Undeveloped Events", 0, child.getId());
			continue;
		}
		else if (typeName == nodetype::INTERMEDIATEEVENT)
		{
			// TODO
		}

		// Static Gates...
		else if (typeName == nodetype::AND)				current = make_shared<ANDGate>(id);
		else if (typeName == nodetype::OR)				current = make_shared<ORGate>(id);
		else if (typeName == nodetype::XOR)				current = make_shared<XORGate>(id);
		else if (typeName == nodetype::VOTINGOR)		current = make_shared<VotingORGate>(id, child.getKOutOfN());
		
		// Dynamic gates...
		else if (typeName == nodetype::FDEP)
		{
 			const string trigger = child.getTriggerId();
// 			std::vector<string> dependentEvents;
// 			for (const string& e : fdep.triggeredEvents())
// 				dependentEvents.emplace_back(e);
// 			current = make_shared<FDEPGate>(id, trigger, dependentEvents);
		}
		else if (typeName == nodetype::PAND)
		{
// 			const faulttree::PriorityAnd& pand = static_cast<const faulttree::PriorityAnd&>(child);
// 			std::vector<string> eventSequence;
// 			for (const string& e : pand.eventSequence())
// 				eventSequence.emplace_back(e);
// 			current = make_shared<PANDGate>(id, eventSequence); 
		}
		else if (typeName == nodetype::SEQ)
		{
// 			const faulttree::Sequence& seq = static_cast<const faulttree::Sequence&>(child);
// 			std::vector<string> eventSequence;
// 			for (const string& e : seq.eventSequence())
// 				eventSequence.emplace_back(e);
// 			current = make_shared<SEQGate>(id, eventSequence); 
		}
		else if (typeName == nodetype::SPARE)
		{
// 			const faulttree::Spare& spareGate = static_cast<const faulttree::Spare&>(child);
// 			if (spareGate.children().size() < 2)
// 				throw std::runtime_error("Spare gates need at least two child nodes");
// 			current = make_shared<SpareGate>(id, spareGate.primaryID(), spareGate.dormancyFactor()); 
		}

		if (current)
		{
			if (!alreadyAdded)
				node->addChild(current);
			convertFaultTreeRecursive(current, child, missionTime);
		}
		else
		{
			convertFaultTreeRecursive(node, child, missionTime);
		}
	}
}