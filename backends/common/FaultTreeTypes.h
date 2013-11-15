#pragma once

#include <typeinfo>
#include "faulttree.h"

using std::type_info;

namespace faultTreeType
{
	extern const type_info* AND;
	extern const type_info* OR;
	extern const type_info* XOR;
	extern const type_info* VOTINGOR;

	extern const type_info* CRISPPROB;
	extern const type_info* FAILURERATE;
	// extern const type_info* FUZZYPROB;

	extern const type_info* BASICEVENT;
	extern const type_info* INTERMEDIATEEVENT;
	extern const type_info* HOUSEEVENT;
	extern const type_info* UNDEVELOPEDEVENT;

	extern const type_info* BASICEVENTSET;

	extern const type_info* FDEP;
	extern const type_info* SPARE;
	extern const type_info* PAND;
	extern const type_info* SEQ;

	extern const type_info* TRANSFERIN;
}