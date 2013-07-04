#include "TreeHelpers.h"
#include "FuzzTreeTypes.h"
#include <typeinfo>
#include <iostream>

using std::string;

faulttree::BasicEvent treeHelpers::copyBasicEvent(const fuzztree::BasicEvent& be)
{
	faulttree::BasicEvent res(be.id(), copyProbability(be.probability()));
	res.name() = be.name();
	return res;
}

faulttree::CrispProbability treeHelpers::copyProbability(const fuzztree::Probability& prob)
{
	using namespace fuzztreeType;

	if (typeid(prob).name() == CRISPPROB)
		return faulttree::CrispProbability(static_cast<const fuzztree::CrispProbability&>(prob).value());
	else
		return faulttree::CrispProbability(0); // TODO
}

faulttree::TopEvent treeHelpers::copyTopEvent(const fuzztree::TopEvent& topEvent)
{
	faulttree::TopEvent res(topEvent.id());
	res.name() = topEvent.name();
	return res;
}

void treeHelpers::printTree(const faulttree::Node& node, int indent)
{
	int i = 0;
	while (i++ < indent)
		std::cout << "   ";
	
	std::cout 
		<< typeid(node).name() << " " 
		<< node.id() << " " 
		<< node.name() << " "
		<< node.children().size() 
		<< std::endl;
	
	++indent;

	for (const auto& child : node.children())
		printTree(child, indent);
}

void treeHelpers::printTree(const fuzztree::Node& node, int indent)
{
	int i = 0;
	while (i++ < indent)
		std::cout << "   ";
	
	std::cout 
		<< typeid(node).name() << " " 
		<< node.id() << " " 
		<< node.name() << " "
		<< node.children().size() 
		<< std::endl;

	++indent;

	for (const auto& child : node.children())
		printTree(child, indent);
}