#pragma once

/************************************************************************/
/* To implement custom behaviour on Fault- or Fuzztrees,                */
/* derive from this class and implement visit() for all subclasses.		*/
/************************************************************************/

#define VISITOR(NodeType)\
	class Visitor\
	{\
	public:\
		virtual void visit(NodeType*) = 0;\
	};\


namespace faulttree
{
	class Node_base;
	template<typename Node_base> class Visitable;
	VISITOR(Visitable<Node_base>)
}


namespace fuzztree
{
	class Node_base;
	template<typename Node_base> class Visitable;
	VISITOR(Visitable<Node_base>)
}