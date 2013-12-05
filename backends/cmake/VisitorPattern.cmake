if (VARIADIC_TEMPLATES)
	# the following options, which generate a tree visitor, need C++0x support for variadic templates
	# GCC >= 4.7 and Intel 13.0 support it, but not VS2012...

	set(TREE_CUSTOMIZATION_ARGS
		--custom-type Node=FaultTreeVisitable<Node_base>/Node_base
		--custom-type TopEvent=FaultTreeVisitable<TopEvent_base>/TopEvent_base
		--custom-type BasicEvent=FaultTreeVisitable<BasicEvent_base>/BasicEvent_base
		--custom-type HouseEvent=FaultTreeVisitable<HouseEvent_base>/HouseEvent_base
		--custom-type UndevelopedEvent=FaultTreeVisitable<UndevelopedEvent_base>/UndevelopedEvent_base
		--custom-type IntermediateEvent=FaultTreeVisitable<IntermediateEvent_base>/IntermediateEvent_base
		--custom-type ChildNode=FaultTreeVisitable<ChildNode_base>/ChildNode_base
		--custom-type Gate=FaultTreeVisitable<Gate_base>/Gate_base
		--custom-type And=FaultTreeVisitable<And_base>/And_base
		--custom-type Or=FaultTreeVisitable<Or_base>/Or_base
		--custom-type Xor=FaultTreeVisitable<Xor_base>/Xor_base
		--custom-type VotingOr=FaultTreeVisitable<VotingOr_base>/VotingOr_base
		--custom-type DynamicGate=FaultTreeVisitable<DynamicGate_base>/DynamicGate_base
		--custom-type Spare=FaultTreeVisitable<Spare_base>/Spare_base
		--custom-type FDEP=FaultTreeVisitable<FDEP_base>/FDEP_base
		--custom-type Sequence=FaultTreeVisitable<Sequence_base>/Sequence_base
		--custom-type PriorityAnd=FaultTreeVisitable<PriorityAnd_base>/PriorityAnd_base
	--fwd-prologue "#include <Visitable.h>"
	)

	set(FUZZTREE_CUSTOMIZATION_ARGS
		--custom-type Node=FuzzTreeVisitable<Node_base>/Node_base
		--custom-type TopEvent=FuzzTreeVisitable<TopEvent_base>/TopEvent_base
		--custom-type BasicEvent=FuzzTreeVisitable<BasicEvent_base>/BasicEvent_base
		--custom-type HouseEvent=FuzzTreeVisitable<HouseEvent_base>/HouseEvent_base
		--custom-type UndevelopedEvent=FuzzTreeVisitable<UndevelopedEvent_base>/UndevelopedEvent_base
		--custom-type IntermediateEvent=FuzzTreeVisitable<IntermediateEvent_base>/IntermediateEvent_base
		--custom-type ChildNode=FuzzTreeVisitable<ChildNode_base>/ChildNode_base
		--custom-type Gate=FuzzTreeVisitable<Gate_base>/Gate_base
		--custom-type And=FuzzTreeVisitable<And_base>/And_base
		--custom-type Or=FuzzTreeVisitable<Or_base>/Or_base
		--custom-type Xor=FuzzTreeVisitable<Xor_base>/Xor_base
		--custom-type VotingOr=FuzzTreeVisitable<VotingOr_base>/VotingOr_base
		--custom-type DynamicGate=FuzzTreeVisitable<DynamicGate_base>/DynamicGate_base
		--custom-type Spare=FuzzTreeVisitable<Spare_base>/Spare_base
		--custom-type FDEP=FuzzTreeVisitable<FDEP_base>/FDEP_base
		--custom-type Sequence=FuzzTreeVisitable<Sequence_base>/Sequence_base
		--custom-type PriorityAnd=FuzzTreeVisitable<PriorityAnd_base>/PriorityAnd_base
		--custom-type RedundancyVariationPoint=FuzzTreeVisitable<RedundancyVariationPoint_base>/RedundancyVariationPoint_base
		--custom-type FeatureVariationPoint=FuzzTreeVisitable<FeatureVariationPoint_base>/FeatureVariationPoint_base
		--custom-type VariationPoint=FuzzTreeVisitable<VariationPoint_base>/VariationPoint_base
		--custom-type IntermediateEventSet=FuzzTreeVisitable<IntermediateEventSet_base>/IntermediateEventSet_base
		--custom-type BasicEventSet=FuzzTreeVisitable<BasicEventSet_base>/BasicEventSet_base
	--fwd-prologue "#include <Visitable.h>"
	)

endif(VARIADIC_TEMPLATES)