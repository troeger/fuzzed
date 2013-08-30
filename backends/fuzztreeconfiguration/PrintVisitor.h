#pragma once
#include "Visitor.h"
#include "faulttree.h"

class PrintVisitor : public faulttree::Visitor
{
public:
	virtual void visit(faulttree::Node&);
	virtual void visit(faulttree::ChildNode&);
	virtual void visit(faulttree::TopEvent&);
	virtual void visit(faulttree::Gate&);
	virtual void visit(faulttree::And&);
	virtual void visit(faulttree::BasicEvent&);
};