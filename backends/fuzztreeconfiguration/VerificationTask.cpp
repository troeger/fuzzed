#include "VerificationTask.h"
#include "FuzzTreeTypes.h"


namespace
{
	const std::string INVALID_DECOMPOSITION_NUMBER	= "Decomposition number is <= 0";
	const std::string TOP_EVENT_CHILD_COUNT_NOT_1	= "Top event may only have a single child";

	// TODO:
// 		DECOMPOSITION_NUMBER_INVALID				(90),	// Decomposition number is <= 0
// 		TOP_EVENT_MISSING							(100),	// There is no top event
// 		TOP_EVENT_CHILD_COUNT_NOT_1					(110),	// Top event may only have a single child
// 		TOP_EVENT_NO_EVENT_SET_CHILD				(115),	// Top event may not have an Event Set as child
// 		GATE_HAS_NO_CHILDREN						(120),	// Gate must have at least one child
// 		UNDEVELOPED_EVENT_INCLUDED					(130),	// UndevelopedEvent is an invalid element
// 		VOTING_OR_NON_POSITIVE_K					(140), 	// k <= 0
// 		VOTING_OR_K_GREATE_CHILDREN					(150), 	// k > #children
// 		BASIC_EVENT_CHILDREN_NOT_ALLOWED			(160), 	// BasicEvent may not have children
// 		BASIC_EVENT_NO_PROBABILITY					(170),	// BasicEvent requires a probability
// 		BASIC_EVENT_INVALID_CRISP_PROBABILITY		(180), 	// CrispProbability is invalid (not in [0,1])
// 		BASIC_EVENT_INVALID_FUZZY_PROBABILITY		(190), 	// FuzzyProbability is invalid (values not in [0,1] or not a <= b1 <= b2 <= c)
// 		INTERMEDIATE_EVENT_CHILD_COUNT_NOT_1		(200),	// IntermediateEvent may only have a single child
// 		INTERMEDIATE_EVENT_NO_EVENT_SET_CHILD		(210), 	// IntermediateEvent may not have an Event Set as child
// 		EVENT_SET_NOT_OPTIONAL_HERE					(220), 	// Event Set may not be optional here (as child of RVP)
// 		EVENT_SET_QUANTITY_NOT_SET					(230),	// Attribute quantity is not set (> 0)
// 		EVENT_SET_NOT_CHILD_OF_FVP					(240),	// Event Set may not be a child of FVP
// 		FVP_HAS_NO_CHILDREN							(250), 	// FeatureVariation point must have at least one child
// 		RVP_CHILD_COUNT_NOT_1						(260), 	// RVP may only have a single child
// 		RVP_INVALID_CHILD							(270), 	// RedundancyVariationPoint may only have Event Sets as children
// 		RVP_FROM_GREATER_TO							(280), 	// From > to
// 		RVP_N_FORMULA_NOT_SET						(290), 	// N-formula not set
// 		RVP_INVALID_N_FORMULA						(300), 	// N-formula produced invalid results (invalid formula or non-integer values)
// 		TRANSFER_IN_CHILDREN_NOT_ALLOWED			(310), 	// Transfer-In may not have children
// 		TRANSFER_IN_ANNOTATION_COUNT_NOT_1			(320),	// Element may only have a single TransferInResult annotation
// 		TRANSFER_IN_ANNOTATION_INVALID				(330), 	// AnalysisResult missing or invalid
// 		TRANSFER_IN_ANNOTATION_DECOMPOSITION_NUMBER	(340), 	// The decomposition number of the attached AnalysisResult does not match
// 		TRANSFER_IN_ANNOTATION_NO_SUITABLE			(350),	// Referenced model does not have a configuration that is cheaper than the specified cost limit.
// 
// 		;
}


VerificationTask::VerificationTask(fuzztree::TopEvent& tree)
	: m_tree(tree)
{}

VerificationResult VerificationTask::compute()
{
	VerificationResult res;

	if (m_tree.children().empty())
		return res; // TODO warning that tree is empty?

	else if (m_tree.children().size() > 1)
		res.addWarning(TOP_EVENT_CHILD_COUNT_NOT_1);

	const auto startingNode = m_tree.children().front();
	computeRecursive(res, startingNode); // TODO: std::async
	
	return res;
}

void VerificationTask::computeRecursive(VerificationResult& res, const fuzztree::ChildNode& node)
{
	using namespace fuzztreeType;

	const type_info& typeName = typeid(node);
	if (isGate(typeName))
	{

	}
	else if (typeName == *BASICEVENT)
	{

	}
	else if (typeName == *INTERMEDIATEEVENT)
	{

	}
}
