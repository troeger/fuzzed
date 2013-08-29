#pragma once

#include "faulttree-fwd.hxx"
#include "fuzztree-fwd.hxx"
#include "Visitable.h"

namespace faulttree
{
	class Visitor
	{
	public:
		virtual void visit(Node&) = 0;
		virtual void visit(ChildNode&) = 0;

		virtual void visit(BasicEvent&) = 0;
		virtual void visit(TopEvent&) = 0;
		virtual void visit(HouseEvent&) = 0;
		virtual void visit(UndevelopedEvent&) = 0;
		virtual void visit(IntermediateEvent&) = 0;

		virtual void visit(Gate&) = 0;
		virtual void visit(DynamicGate&) = 0;

		virtual void visit(And&) = 0;
		virtual void visit(Or&) = 0;
		virtual void visit(Xor&) = 0;
		virtual void visit(VotingOr&) = 0;

		virtual void visit(Spare&) = 0;
		virtual void visit(FDEP&) = 0;
		virtual void visit(PriorityAnd&) = 0;
		virtual void visit(Sequence&) = 0;
	};
}

namespace fuzztree
{
	class Visitor
	{
	public:
		virtual void visit(Node&) = 0;
		virtual void visit(ChildNode&) = 0;

		virtual void visit(BasicEvent&) = 0;
		virtual void visit(TopEvent&) = 0;
		virtual void visit(HouseEvent&) = 0;
		virtual void visit(UndevelopedEvent&) = 0;
		virtual void visit(IntermediateEvent&) = 0;

		virtual void visit(Gate&) = 0;

		virtual void visit(And&) = 0;
		virtual void visit(Or&) = 0;
		virtual void visit(Xor&) = 0;
		virtual void visit(VotingOr&) = 0;

		virtual void visit(VariationPoint&) = 0;
		virtual void visit(RedundancyVariationPoint&) = 0;
		virtual void visit(FeatureVariationPoint&) = 0;

		virtual void visit(IntermediateEventSet&) = 0;
		virtual void visit(BasicEventSet&) = 0;
	};
}

template <typename Base>
void FaultTreeVisitable<Base>::accept(faulttree::Visitor& visitor)
{
	visitor.visit(static_cast< FaultTreeVisitable<Base>& >(*this));
}

template <typename Base>
void FuzzTreeVisitable<Base>::accept(fuzztree::Visitor& visitor)
{
	visitor.visit(static_cast< FuzzTreeVisitable<Base>& >(*this));
}

#define RECURSE_VISITOR(n)\
	for (auto& child : n.children()) child.accept(*this);