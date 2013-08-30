#include "PrintVisitor.h"
#include <iostream>

using namespace std;
using namespace faulttree;

void PrintVisitor::visit(BasicEvent& b)
{
	cout << "BasicEvent" << endl;
	RECURSE_VISITOR(b)
}

void PrintVisitor::visit(Node& n)
{
	cout << "Node" << endl;
	RECURSE_VISITOR(n)
}

void PrintVisitor::visit(ChildNode& c)
{
	cout << "Child" << endl;
	RECURSE_VISITOR(c)
}

void PrintVisitor::visit(Gate& g)
{
	cout << "Gate" << endl;
	RECURSE_VISITOR(g)
}

void PrintVisitor::visit(TopEvent& t)
{
	cout << "TopEvent" << endl;
	RECURSE_VISITOR(t)
}

void PrintVisitor::visit(And& a)
{
	cout << "AndGate" << endl;
	RECURSE_VISITOR(a)
}
