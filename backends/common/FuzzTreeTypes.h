#pragma once

#include <typeinfo>
#include "fuzztree.h"

using std::type_info;

namespace fuzztreeType
{
	extern const type_info* AND;
	extern const type_info* OR;
	extern const type_info* XOR;
	extern const type_info* VOTINGOR;

	extern const type_info* BASICEVENTSET;
	extern const type_info* INTERMEDIATEEVENTSET;
	extern const type_info* REDUNDANCYVP;
	extern const type_info* INCLUSIONVP;
	extern const type_info* FEATUREVP;

	extern const type_info* CRISPPROB;
	extern const type_info* FAILURERATE;
	extern const type_info* FUZZYPROB;

	extern const type_info* BASICEVENT;
	extern const type_info* INTERMEDIATEEVENT;
	extern const type_info* HOUSEEVENT;
	extern const type_info* UNDEVELOPEDEVENT;

// 	const type_info* FDEP	= &typeid(fuzztree::FDEP);
// 	const type_info* SPARE	= &typeid(fuzztree::Spare);
// 	const type_info* PAND	= &typeid(fuzztree::PriorityAnd);
// 	const type_info* SEQ	= &typeid(fuzztree::Sequence);
}