#pragma once

namespace fuzztreeType
{
	const std::string AND		= "class fuzztree::And";
	const std::string OR		= "class fuzztree::Or";
	const std::string XOR		= "class fuzztree::Xor";
	const std::string VOTINGOR	= "class fuzztree::VotingOr";

	const std::string BASICEVENTSET			= "class fuzztree::BasicEventSet";
	const std::string INTERMEDIATEEVENTSET	= "class fuzztree::IntermediateEventSet";

	const std::string BASICEVENT		= "class fuzztree::BasicEvent";
	const std::string INTERMEDIATEEVENT	= "class fuzztree::IntermediateEvent";
	const std::string HOUSEEVENT		= "class fuzztree::HouseEvent";
	const std::string UNDEVELOPEDEVENT	= "class fuzztree::UndevelopedEvent";

	const std::string REDUNDANCYVP	= "class fuzztree::RedundancyVariationPoint";
	const std::string INCLUSIONVP	= "class fuzztree::InclusionVariationPoint";
	const std::string FEATUREVP		= "class fuzztree::FeatureVariationPoint";

	const std::string CRISPPROB		= "class fuzztree::CrispProbability";
	const std::string FAILURERATE	= "class fuzztree::FailureRate";
	const std::string FUZZYPROB		= "class fuzztree::DecomposedFuzzyProbability";
}