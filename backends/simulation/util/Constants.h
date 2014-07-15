#pragma once

const std::string EMPTY = "";
const char* const NOT_IMPLEMENTED = "not yet implemented";

/************************************************************************/
/* XML Tags                                                             */
/************************************************************************/

namespace PNML
{
	const char* const PNML_EXT = ".pnml";
	const char* const TRANSITION_TAG = "transition";
	const char* const PLACE_TAG = "place";
	const char* const ARC_TAG = "arc";
	const char* const MEASURE_TAG = "measure";
	const char* const RATE_TAG = "rate";
	const char* const PRIORITY_TAG = "priority";
	const char* const TIMED_TAG = "timed";
	const char* const VALUE_TAG = "value";
	const char* const NAME_TAG = "name";
	const char* const LABEL_TAG = "label";
	const char* const ROOT_TAG = "net";
	const char* const PNML_TAG = "pnml";
	const char* const INSCRIPTION_TAG = "inscription";
	const char* const TYPE_TAG = "type";
	const char* const INHIBITOR_ATTR = "inhibitor";
	const char* const INITIALMARKING_TAG = "initialMarking";
	const char* const TOPLEVEL_TAG = "isTopLevelEvent";
	const char* const CONSTRAINT_TAG = "isConstraintPlace";
	const char* const CAPACITY_TAG = "capacity";
	const char* const SOURCE_TAG = "source";
	const char* const TARGET_TAG = "target";
	const char* const TOOL_SPECIFIC_TAG = "toolSpecific";
	const char* const SEQUENCE_CONSTRAINT = "sequenceConstraint";
	const char* const SEQUENCE_LIST = "sequence";
}

const char* const USER_DESCRIPTION_LABEL = "userDescription";

const char* const FAILURE_LABEL = "SystemFailure";

const char* const TRANSITION_IDENTIFIER = "T"; 
const char* const PLACE_IDENTIFIER = "p";
const char* const ARC_IDENTIFIER = "a";

const char* const ID_ATTRIBUTE = "id";


/************************************************************************/
/* FuzzTree-Format                                                      */
/************************************************************************/

namespace faultTree
{
	const char* const FAULT_TREE = "ft:FaultTree";
	const char* const FAULT_TREE_EXT = ".faulttree";
	const char* const TOP_EVENT = "topEvent";

	const char* const BASIC_EVENT = "ft:BasicEvent";
	const char* const UNDEVELOPED_EVENT = "ft:UndevelopedEvent";
	const char* const INTERMEDIATE_EVENT = "ft:IntermediateEvent";

	const char* const AND_GATE = "ft:And";
	const char* const OR_GATE = "ft:Or";
	const char* const XOR_GATE = "ft:Xor";
	const char* const VOTING_OR_GATE = "ft:VotingOr";

	const char* const COLD_SPARE_GATE = "ft:ColdSpare";
	const char* const PAND_GATE = "ft:PriorityAnd";
	const char* const SEQ_GATE = "ft:Sequence";
	const char* const FDEP_GATE = "ft:FDEP";

	const char* const CRISP_NUM = "ft:CrispProbability";
	const char* const SPARE_ID_ATTRIBUTE = "spareIds";
	const char* const PRIO_ID_ATTRIBUTE = "priorityIds";

	const char* const CHILDREN = "children";
	const char* const NODE_TYPE = "xsi:type";
	const char* const NAME_ATTRIBUTE = "name";
	const char* const VOTING_OR_K = "k";
	const char* const SEQUENCE_ATTRIBUTE = "eventSequence";
}

namespace fuzzTree
{
	const char* const FUZZ_TREE = "ft:FuzzTree";
	const char* const FUZZ_TREE_EXT = ".fuzztree"; 

	const char* const BASIC_EVENT_SET = "ft:BasicEventSet";
	const char* const TRANSFER_GATE = "ft:TransferIn";
	const char* const FEATURE_VP = "ft:FeatureVariationPoint";
	const char* const REDUNDANCY_VP = "ft:RedundancyVariationPoint";

	const char* const TRIANGULAR_FUZZY_NUM = "TriangularFuzzyInterval";

	const char* const OPTIONAL_ATTRIBUTE = "optional";
	const char* const COST_ATTRIBUTE = "cost";
	const char* const BASIC_EVENT_SET_QUANTITY = "quantity";
	const char* const REDUNDANCY_FORMULA = "formula";
}