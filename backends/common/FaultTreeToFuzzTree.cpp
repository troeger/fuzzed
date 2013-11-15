#include "FaultTreeToFuzzTree.h"

#include "faulttree.h"
#include "FaultTreeTypes.h"
#include "fuzztree.h"
#include "FuzzTreeTypes.h"

#include "util.h"
#include "xmlutil.h"

std::shared_ptr<fuzztree::TopEvent> faultTreeToFuzzTree(const faulttree::TopEvent& faultTree, std::vector<Issue>& issues)
{
	int missionTime = faultTree.missionTime().present() ? faultTree.missionTime().get() : DEFAULT_MISSION_TIME;
	int decompositionNumber = faultTree.decompositionNumber().present() ? faultTree.decompositionNumber().get() : DEFAULT_DECOMPOSITION_NUMBER;

	std::shared_ptr<fuzztree::TopEvent> top(new fuzztree::TopEvent(faultTree.id()));

	top->missionTime(missionTime);
	top->decompositionNumber(decompositionNumber);
	
	faultTreeToFuzzTreeRecursive(*(top.get()), faultTree, issues);
	return top;
}


void faultTreeToFuzzTreeRecursive(fuzztree::Node& node, const faulttree::Node& templateNode, std::vector<Issue>& issues)
{
	using namespace faultTreeType;

	for (const auto& child : templateNode.children())
	{
		const string id = child.id();
		const type_info& typeName = typeid(child);

		// Leaf nodes...
		if (typeName == *BASICEVENT) 
		{
			const auto& prob = (static_cast<const faulttree::BasicEvent&>(child)).probability();
			const type_info& probName = typeid(prob);

			if (probName == *CRISPPROB)
			{
				const auto probabilityValue = static_cast<const faulttree::CrispProbability&>(prob).value();
				node.children().push_back(fuzztree::BasicEvent(id, fuzztree::CrispProbability(probabilityValue)));
			}
			else
			{
				const auto failureRate = static_cast<const faulttree::FailureRate&>(prob).value();
				node.children().push_back(fuzztree::BasicEvent(id, fuzztree::FailureRate(failureRate)));
			}
		}
		else if (typeName == *BASICEVENTSET)
		{
			const auto& bes = static_cast<const faulttree::BasicEventSet&>(child);
			const auto& prob = bes.probability();
			const type_info& probName = typeid(prob);
			const int quantity = bes.quantity().present() ? bes.quantity().get() : 1; // TODO: in fault trees, the quantity should not be optional

			if (probName == *CRISPPROB)
			{
				const auto probabilityValue = static_cast<const faulttree::CrispProbability&>(prob).value();
				for (int i = 0;  i < quantity; ++i)
				{
					node.children().push_back(fuzztree::BasicEvent(id + "." + util::toString(i), fuzztree::CrispProbability(probabilityValue)));
				}
			}
			else
			{
				const auto failureRate = static_cast<const faulttree::FailureRate&>(prob).value();
				for (int i = 0;  i < quantity; ++i)
				{
					node.children().push_back(fuzztree::BasicEvent(id + "." + util::toString(i), fuzztree::FailureRate(failureRate)));
				}
			}

			// TODO: FDEPs might trigger an entire event set... this continue doesn't work then...
			continue;
		}
		else if (typeName == *HOUSEEVENT)
		{ // TODO find out if this is legitimate
			const auto& prob = (static_cast<const faulttree::BasicEvent&>(child)).probability();
			const type_info& probName = typeid(prob);

			if (probName == *CRISPPROB)
			{
				const auto probabilityValue = static_cast<const faulttree::CrispProbability&>(prob).value();
				node.children().push_back(fuzztree::HouseEvent(id, fuzztree::FailureRate(probabilityValue)));
			}
			else
			{
				const auto failureRate = static_cast<const faulttree::FailureRate&>(prob).value();
				node.children().push_back(fuzztree::HouseEvent(id, fuzztree::FailureRate(failureRate)));
			}

			continue;
		}
		else if (typeName == *UNDEVELOPEDEVENT)
		{
			node.children().push_back(fuzztree::UndevelopedEvent(id));
			continue;
		}
		else if (typeName == *INTERMEDIATEEVENT)
		{
			node.children().push_back(fuzztree::IntermediateEvent(id));
		}
		else if (typeName == *TRANSFERIN)
		{
			issues.emplace_back("TransferIn is not yet supported.", 0, id);
			continue; // TODO as issue
		}

		// Static Gates...
		else if (typeName == *AND)				node.children().push_back(fuzztree::And(id));
		else if (typeName == *OR)				node.children().push_back(fuzztree::Or(id));
		else if (typeName == *XOR)				node.children().push_back(fuzztree::Xor(id));
		else if (typeName == *VOTINGOR)			node.children().push_back(fuzztree::VotingOr(id, static_cast<const faulttree::VotingOr&>(child).k()));
		

		faultTreeToFuzzTreeRecursive(node.children().back(), child, issues);
	}
}