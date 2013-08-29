#pragma once

#include "faulttree-fwd.hxx"
#include "fuzztree-fwd.hxx"
#include "Visitable.h"

namespace faulttree
{
	class Visitor
	{
	public:
		virtual void visit(Node& n) = 0;
	};
}

namespace fuzztree
{
	class Visitor
	{
	public:
		virtual void visit(Node& n) = 0;
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