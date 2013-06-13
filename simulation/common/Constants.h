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

const char* const TRANSITION_IDENTIFIER = "t"; 
const char* const PLACE_IDENTIFIER = "p";
const char* const ARC_IDENTIFIER = "a";

const std::string g_alphabet = "abcdefghijklmnopqrstuvwxyz";

const char* const ID_ATTRIBUTE = "id";


/************************************************************************/
/* FuzzTree-Format                                                      */
/************************************************************************/

namespace faultTree
{
	const char* const FAULT_TREE = "FaultTree";
	const char* const FAULT_TREE_EXT = ".faulttree";
	const char* const TOP_EVENT = "topEvent";

	const char* const BASIC_EVENT = "BasicEvent";
	const char* const UNDEVELOPED_EVENT = "UndevelopedEvent";
	const char* const INTERMEDIATE_EVENT = "IntermediateEvent";

	const char* const AND_GATE = "And";
	const char* const OR_GATE = "Or";
	const char* const XOR_GATE = "Xor";
	const char* const VOTING_OR_GATE = "VotingOr";

	const char* const COLD_SPARE_GATE = "ColdSpare";
	const char* const PAND_GATE = "PriorityAnd";
	const char* const SEQ_GATE = "Sequence";
	const char* const FDEP_GATE = "FDEP";

	const char* const CRISP_NUM = "CrispProbability";
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
	const char* const FUZZ_TREE = "FuzzTree";
	const char* const FUZZ_TREE_EXT = ".fuzztree"; 

	const char* const BASIC_EVENT_SET = "BasicEventSet";
	const char* const TRANSFER_GATE = "TransferIn";
	const char* const FEATURE_VP = "FeatureVariationPoint";
	const char* const REDUNDANCY_VP = "RedundancyVariationPoint";

	const char* const TRIANGULAR_FUZZY_NUM = "TriangularFuzzyInterval";

	const char* const OPTIONAL_ATTRIBUTE = "optional";
	const char* const COST_ATTRIBUTE = "cost";
	const char* const BASIC_EVENT_SET_QUANTITY = "quantity";
	const char* const REDUNDANCY_FORMULA = "formula";
}

namespace simulation
{
	const char* const SIMULATION_RESULT = "fts:SimulationResult";
	const char* const SIMULATION_ERROR = "error";
	const char* const SIMULATION_WARNING = "warning";
	const char* const SIMULATION_MESSAGE = "message";
	
	// attributes
	const char* const RELIABILITY = "reliability";
	const char* const AVAILABILTIY = "availability";
	const char* const NROUNDS = "nSimulatedRounds";
	const char* const MTTF = "mttf";
	const char* const NFAILURES = "nFailures";
	const char* const MODELID = "modelId";
	const char* const TIMESTAMP = "timestamp";
	const char* const DURATION = "duration";
}