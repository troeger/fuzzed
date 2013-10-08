#include "FuzzTreeTypes.h"

namespace fuzztreeType
{
	const type_info* AND	= &typeid(fuzztree::And);
	const type_info* OR		= &typeid(fuzztree::Or);
	const type_info* XOR	= &typeid(fuzztree::Xor);
	const type_info* VOTINGOR = &typeid(fuzztree::VotingOr);

	const type_info* BASICEVENTSET			= &typeid(fuzztree::BasicEventSet);
	const type_info* INTERMEDIATEEVENTSET	= &typeid(fuzztree::IntermediateEventSet);
	const type_info* REDUNDANCYVP			= &typeid(fuzztree::RedundancyVariationPoint);
	const type_info* INCLUSIONVP			= &typeid(fuzztree::InclusionVariationPoint);
	const type_info* FEATUREVP				= &typeid(fuzztree::FeatureVariationPoint);

	const type_info* CRISPPROB		= &typeid(fuzztree::CrispProbability);
	const type_info* FAILURERATE	= &typeid(fuzztree::FailureRate);
	const type_info* TRIANGULARFUZZYINTERVAL = &typeid(fuzztree::TriangularFuzzyInterval);
	const type_info* DECOMPOSEDFUZZYINTERVAL = &typeid(fuzztree::DecomposedFuzzyProbability);

	const type_info* BASICEVENT			= &typeid(fuzztree::BasicEvent);
	const type_info* INTERMEDIATEEVENT	= &typeid(fuzztree::IntermediateEvent);
	const type_info* HOUSEEVENT			= &typeid(fuzztree::HouseEvent);
	const type_info* UNDEVELOPEDEVENT	= &typeid(fuzztree::UndevelopedEvent);

// 	const type_info* FDEP	= &typeid(fuzztree::FDEP);
// 	const type_info* SPARE	= &typeid(fuzztree::Spare);
// 	const type_info* PAND	= &typeid(fuzztree::PriorityAnd);
// 	const type_info* SEQ	= &typeid(fuzztree::Sequence);

	bool isGate(const type_info& typeName)
	{
		return
			typeName == *AND ||
			typeName == *OR ||
			typeName == *XOR ||
			typeName == *VOTINGOR;
	}

	bool isLeaf(const type_info& typeName)
	{
		return
			typeName == *BASICEVENT ||
			typeName == *HOUSEEVENT ||
			typeName == *UNDEVELOPEDEVENT ||
			typeName == *BASICEVENTSET;
	}


	bool isVariationPoint(const type_info& typeName)
	{
		return
			typeName == *FEATUREVP ||
			typeName == *REDUNDANCYVP;
	}

	bool isEventSet(const type_info& typeName)
	{
		return
			typeName == *BASICEVENTSET ||
			typeName == *INTERMEDIATEEVENTSET;
	}
}