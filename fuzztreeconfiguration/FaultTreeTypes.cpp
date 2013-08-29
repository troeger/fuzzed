#include "FaultTreeTypes.h"

namespace faultTreeType
{
	const type_info* AND	= &typeid(faulttree::And);
	const type_info* OR		= &typeid(faulttree::Or);
	const type_info* XOR	= &typeid(faulttree::Xor);
	const type_info* VOTINGOR = &typeid(faulttree::VotingOr);

	const type_info* CRISPPROB		= &typeid(faulttree::CrispProbability);
	const type_info* FAILURERATE	= &typeid(faulttree::FailureRate);
	const type_info* FUZZYPROB		= &typeid(faulttree::DecomposedFuzzyProbability);

	const type_info* BASICEVENT			= &typeid(faulttree::BasicEvent);
	const type_info* INTERMEDIATEEVENT	= &typeid(faulttree::IntermediateEvent);
	const type_info* HOUSEEVENT			= &typeid(faulttree::HouseEvent);
	const type_info* UNDEVELOPEDEVENT	= &typeid(faulttree::UndevelopedEvent);

	const type_info* FDEP	= &typeid(faulttree::FDEP);
	const type_info* SPARE	= &typeid(faulttree::Spare);
	const type_info* PAND	= &typeid(faulttree::PriorityAnd);
	const type_info* SEQ	= &typeid(faulttree::Sequence);
}