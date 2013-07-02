#include "TreeHelpers.h"
#include <typeinfo>
#include <iostream>

faulttree::BasicEvent treeHelpers::copyBasicEvent(const fuzztree::BasicEvent& be)
{
	faulttree::BasicEvent res(be.id(), copyProbability(be.probability()));
	res.name() = be.name();
	return res;
}

faulttree::Gate treeHelpers::copyGate(const fuzztree::Node& gate)
{
	faulttree::Gate res("0");
	const fuzztree::And* andGate = dynamic_cast<const fuzztree::And*>(&gate);
	if (andGate) 
		res = faulttree::And(andGate->id());

	const fuzztree::Or* orGate = dynamic_cast<const fuzztree::Or*>(&gate);
	if (orGate) 
		res = faulttree::Or(orGate->id());

	const fuzztree::VotingOr* votingOr = dynamic_cast<const fuzztree::VotingOr*>(&gate);
	if (votingOr) 
		res = faulttree::And(votingOr->id(), votingOr->k());

	const fuzztree::Xor* xorGate = dynamic_cast<const fuzztree::Xor*>(&gate);
	if (xorGate) 
		res = faulttree::Xor(xorGate->id());

	res.name() = gate.name();
	return res;
}

faulttree::Probability treeHelpers::copyProbability(const fuzztree::Probability& prob)
{
	const fuzztree::CrispProbability* crisp = dynamic_cast<const fuzztree::CrispProbability*>(&prob);
	if (crisp) return faulttree::CrispProbability(crisp->value());

	else
	{
		const fuzztree::DecomposedFuzzyProbability* fuzzy = 
			dynamic_cast<const fuzztree::DecomposedFuzzyProbability*>(&prob);
		return faulttree::CrispProbability(0); // TODO
	}
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