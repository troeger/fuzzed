#pragma once

const char* const NOT_IMPLEMENTED = "not yet implemented";

/************************************************************************/
/* XML Tags                                                             */
/************************************************************************/
namespace timeNET
{
	const char* const TIMED_TRANSITION_TAG = "timedTransition";
	const char* const IMMEDIATE_TRANSITION_TAG = "immediateTransition";
	const char* const PLACE_TAG = "place";
	const char* const ARC_TAG = "arc";
	const char* const MEASURE_TAG = "measure";
	const char* const RATE_TAG = "rate";
	const char* const INITIALMARKING_TAG = "initialMarking";
	const char* const ROOT_TAG = "net";
}

namespace PNML
{
	const char* const TRANSITION_TAG = "transition";
	const char* const PLACE_TAG = "place";
	const char* const ARC_TAG = "arc";
	const char* const MEASURE_TAG = "measure";
	const char* const RATE_TAG = "rate";
	const char* const PRIORITY_TAG = "priority";
	const char* const TIMED_TAG = "timed";
	const char* const VALUE_TAG = "value";
	const char* const NAME_TAG = "name";
	const char* const ROOT_TAG = "net";
	const char* const PNML_TAG = "pnml";
	const char* const INSCRIPTION_TAG = "inscription";
	const char* const INITIALMARKING_TAG = "initialMarking";
	const char* const TOPLEVEL_TAG = "isTopLevelEvent";
	const char* const CAPACITY_TAG = "capacity";
	const char* const ID_TAG = "id";
	const char* const SOURCE_TAG = "source";
	const char* const TARGET_TAG = "target";
}

const char* const USER_DESCRIPTION_LABEL = "userDescription";

const char* const FAILURE_LABEL = "SystemFailure";

const char* const TRANSITION_IDENTIFIER = "t"; 
const char* const PLACE_IDENTIFIER = "p";
const char* const ARC_IDENTIFIER = "a";

const std::string g_alphabet = "abcdefghijklmnopqrstuvwxyz";


/************************************************************************/
/* FuzzTree-Format                                                      */
/************************************************************************/
namespace fuzzTree 
{
	const char* const FUZZ_TREE = "ft:FuzzTree";
	const char* const TOP_EVENT = "topEvent";

	const char* const INTERMEDIATE_EVENT = "ft:IntermediateEvent";
	const char* const INTERMEDIATE_EVENT_SET = "ft:IntermediateEventSet";
	const char* const BASIC_EVENT = "ft:BasicEvent";
	const char* const BASIC_EVENT_SET = "ft:BasicEventSet";
	const char* const UNDEVELOPED_EVENT = "ft:UndevelopedEvent";
	const char* const TRANSFER_GATE = "ft:TransferIn";
	const char* const FEATURE_VP = "ft:FeatureVariationPoint";
	const char* const REDUNDANCY_VP = "ft:RedundancyVariationPoint";

	const char* const AND_GATE = "ft:And";
	const char* const OR_GATE = "ft:Or";
	const char* const XOR_GATE = "ft:Xor";
	const char* const VOTING_OR_GATE = "ft:VotingOr";

	const char* const COLD_SPARE_GATE = "ft:ColdSpareGate";
	const char* const PAND_GATE = "ft:PriorityAnd";

	const char* const TRIANGULAR_FUZZY_NUM = "ft:TriangularFuzzyInterval";
	const char* const CRISP_NUM = "ft:CrispProbability";

	// attributes
	const char* const SPARE_ID_ATTRIBUTE = "spareIds";
	const char* const PRIO_ID_ATTRIBUTE = "priorityIds";
	const char* const OPTIONAL_ATTRIBUTE = "optional";
	const char* const COST_ATTRIBUTE = "cost";
	const char* const CHILDREN = "children";
	const char* const NODE_TYPE = "xsi:type";
	const char* const NAME_ATTRIBUTE = "name";
	const char* const VOTING_OR_K = "k";
	const char* const BASIC_EVENT_SET_QUANTITY = "quantity";
}