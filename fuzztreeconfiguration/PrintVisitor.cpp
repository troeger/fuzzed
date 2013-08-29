#include "PrintVisitor.h"
#include <iostream>

using namespace std;
using namespace faulttree;

void PrintVisitor::visit(BasicEvent&)
{
	cout << "BasicEvent" << endl;
}

void PrintVisitor::visit(Node&)
{
	cout << "Node" << endl;
}

void PrintVisitor::visit(Gate&)
{
	cout << "Gate" << endl;
}

void PrintVisitor::visit(TopEvent&)
{
	cout << "Gate" << endl;
}