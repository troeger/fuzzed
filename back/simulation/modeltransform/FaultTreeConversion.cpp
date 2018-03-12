#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"

#include "faulttree.h"
#include "FaultTreeTypes.h"
#include "fuzztree.h"
#include "FuzzTreeTypes.h"

#include "util.h"
#include "xmlutil.h"
#include "FatalException.h"

using std::string;
using std::shared_ptr;
using std::make_shared;

std::shared_ptr<TopLevelEvent> fromGeneratedFaultTree(const faulttree::TopEvent& generatedTree)
{
	unsigned int mt = DEFAULT_MISSION_TIME;
	if (generatedTree.missionTime().present())
		mt = generatedTree.missionTime().get();

	shared_ptr<TopLevelEvent> top(new TopLevelEvent(generatedTree.id(), mt));
	convertFaultTreeRecursive(top, generatedTree, mt);
	return top;
}

void convertFaultTreeRecursive(FaultTreeNode::Ptr node, const faulttree::Node& templateNode, const unsigned int& missionTime)
{
	using namespace faultTreeType;

	FaultTreeNode::Ptr current = nullptr;

	for (const auto& child : templateNode.children())
	{
		const string id = child.id();
		const type_info& typeName = typeid(child);
		bool alreadyAdded = false;
		
		// Leaf nodes...
		if (typeName == *BASICEVENT) 
		{
			const auto& prob = (static_cast<const faulttree::BasicEvent&>(child)).probability();
			const type_info& probName = typeid(prob);
			
			double failureRate = 0.f;
			if (probName == *CRISPPROB)
				failureRate = util::rateFromProbability(static_cast<const faulttree::CrispProbability&>(prob).value(), missionTime);
			else
			{
				assert(dynamic_cast<const faulttree::FailureRate*>(&prob));
				failureRate = static_cast<const faulttree::FailureRate&>(prob).value();
			}
			current = make_shared<BasicEvent>(id, failureRate);
			node->addChild(current);
			alreadyAdded = true;
			
			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == *BASICEVENTSET)
		{
			const auto& bes = static_cast<const faulttree::BasicEventSet&>(child);
			const auto& prob = bes.probability();
			const type_info& probName = typeid(prob);
			const int quantity = bes.quantity().present() ? bes.quantity().get() : 1; // TODO: in fault trees, the quantity should not be optional

			double failureRate = 0.f;
			if (probName == *CRISPPROB)
				failureRate = util::rateFromProbability(static_cast<const faulttree::CrispProbability&>(prob).value(), missionTime);
			else
			{
				assert(dynamic_cast<const faulttree::FailureRate*>(&prob));
				failureRate = static_cast<const faulttree::FailureRate&>(prob).value();
			}

			for (int i = 0; i<quantity; ++i)
			{
				node->addChild(make_shared<BasicEvent>(id, failureRate));
			}
			continue; // TODO these might also be triggered by FDEP
		}
		else if (typeName == *HOUSEEVENT)
		{ // TODO find out if this is legitimate
			current = make_shared<BasicEvent>(id, 0);
			node->addChild(current);
			continue;
		}
		else if (typeName == *UNDEVELOPEDEVENT)
		{
			throw std::runtime_error("Cannot simulate trees with undeveloped events!");
			continue;
		}
		else if (typeName == *INTERMEDIATEEVENT)
		{
			// TODO
		}

		// Static Gates...
		else if (typeName == *AND)				current = make_shared<ANDGate>(id);
		else if (typeName == *OR)				current = make_shared<ORGate>(id);
		else if (typeName == *XOR)				current = make_shared<XORGate>(id);
		else if (typeName == *VOTINGOR)			current = make_shared<VotingORGate>(id, static_cast<const faulttree::VotingOr&>(child).k());
		
		// Dynamic gates...
		else if (typeName == *FDEP)
		{
			const faulttree::FDEP& fdep = static_cast<const faulttree::FDEP&>(child);
			const string trigger = fdep.trigger();
			std::vector<string> dependentEvents;
			for (const string& e : fdep.triggeredEvents())
				dependentEvents.emplace_back(e);
			current = make_shared<FDEPGate>(id, trigger, dependentEvents);
		}
		else if (typeName == *PAND)
		{
			const faulttree::PriorityAnd& pand = static_cast<const faulttree::PriorityAnd&>(child);
			std::vector<string> eventSequence;
			for (const string& e : pand.eventSequence())
				eventSequence.emplace_back(e);
			current = make_shared<PANDGate>(id, eventSequence); 
		}
		else if (typeName == *SEQ)
		{
			const faulttree::Sequence& seq = static_cast<const faulttree::Sequence&>(child);
			std::vector<string> eventSequence;
			for (const string& e : seq.eventSequence())
				eventSequence.emplace_back(e);
			current = make_shared<SEQGate>(id, eventSequence); 
		}
		else if (typeName == *SPARE)
		{
			const faulttree::Spare& spareGate = static_cast<const faulttree::Spare&>(child);
			if (spareGate.children().size() < 2)
				throw std::runtime_error("Spare gates need at least two child nodes");
			current = make_shared<SpareGate>(id, spareGate.primaryID(), spareGate.dormancyFactor()); 
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

std::shared_ptr<TopLevelEvent> fromGeneratedFuzzTree(const fuzztree::TopEvent& generatedTree)
{
	unsigned int mt = DEFAULT_MISSION_TIME;
	if (generatedTree.missionTime().present())
		mt = generatedTree.missionTime().get();

	shared_ptr<TopLevelEvent> top(new TopLevelEvent(generatedTree.id(), mt));
	convertFuzzTreeRecursive(top, generatedTree, mt);
	return top;
}

void convertFuzzTreeRecursive(FaultTreeNode::Ptr node, const fuzztree::Node& templateNode, const unsigned int& missionTime)
{
	using namespace fuzztreeType;

	FaultTreeNode::Ptr current = nullptr;

	for (const auto& child : templateNode.children())
	{
		const string id = child.id();
		const type_info& typeName = typeid(child);
		bool alreadyAdded = false;

		// Leaf nodes...
		if (typeName == *BASICEVENT) 
		{
			const auto& prob = (static_cast<const fuzztree::BasicEvent&>(child)).probability();
			const type_info& probName = typeid(prob);

			double failureRate = 0.f;
			if (probName == *CRISPPROB)
			{
				failureRate = util::rateFromProbability(static_cast<const fuzztree::CrispProbability&>(prob).value(), missionTime);
			}
			else if (probName == *TRIANGULARFUZZYINTERVAL)
			{
				//std::cout << "Encountered fuzzy probability during simulation";
				throw FatalException("Fuzztrees containing fuzzy probabilities cannot be converted to fault trees and thus cannot be simulated.", 0, id);
			}
			else
			{
				assert(dynamic_cast<const fuzztree::FailureRate*>(&prob));
				failureRate = static_cast<const fuzztree::FailureRate&>(prob).value();
			}
			current = make_shared<BasicEvent>(id, failureRate);
			node->addChild(current);
			alreadyAdded = true;

			// BasicEvents can have FDEP children...
			// continue;
		}
		else if (typeName == *HOUSEEVENT)
		{ // TODO find out if this is legitimate
			current = make_shared<BasicEvent>(id, 0);
			node->addChild(current);
			continue;
		}
		else if (typeName == *UNDEVELOPEDEVENT)
		{
			throw std::runtime_error("Cannot simulate trees with undeveloped events!");
			continue;
		}
		else if (typeName == *INTERMEDIATEEVENT)
		{
			current = nullptr;
		}

		// Static Gates...
		else if (typeName == *AND)				current = make_shared<ANDGate>(id);
		else if (typeName == *OR)				current = make_shared<ORGate>(id);
		else if (typeName == *XOR)				current = make_shared<XORGate>(id);
		else if (typeName == *VOTINGOR)			current = make_shared<VotingORGate>(id, static_cast<const fuzztree::VotingOr&>(child).k());

		if (current)
		{
			if (!alreadyAdded)
				node->addChild(current);
			convertFuzzTreeRecursive(current, child, missionTime);
		}
		else
		{
			convertFuzzTreeRecursive(node, child, missionTime);
		}
	}
}
