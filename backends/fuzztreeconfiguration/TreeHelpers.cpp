#include "TreeHelpers.h"
#include "FuzzTreeTypes.h"
#include <typeinfo>
#include <iostream>
#include <iomanip>
#include <stdarg.h>

using std::string;

faulttree::BasicEvent treeHelpers::copyBasicEvent(const fuzztree::BasicEvent& be)
{
	const auto& prob = be.probability();
	
	faulttree::BasicEvent res(
		be.id(),
		typeid(prob) == *fuzztreeType::CRISPPROB ? 
			faulttree::CrispProbability(static_cast<const fuzztree::CrispProbability&>(prob).value()) :
			faulttree::CrispProbability(0));

	res.name() = be.name();
	return res;
}

faulttree::TopEvent treeHelpers::copyTopEvent(const fuzztree::TopEvent& topEvent)
{
	faulttree::TopEvent res(topEvent.id());
	res.missionTime() = topEvent.missionTime();
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

std::string treeHelpers::toString(const double& d, const int& prec /*= 5*/)
{
	std::ostringstream oss;
	oss << std::fixed << std::setprecision(prec);
	oss << d;
	return oss.str();
}

std::string treeHelpers::toString(const long double& d, const int& prec /*= 5*/)
{
	std::ostringstream oss;
	oss << std::fixed << std::setprecision(prec);
	oss << d;
	return oss.str();
}

std::string treeHelpers::toString(const int& d)
{
	std::ostringstream oss;
	oss << d;
	return oss.str();
}

void treeHelpers::replaceStringInPlace(string& subject, const string& search, const std::string& replacement)
{
	size_t pos = 0;
	while ((pos = subject.find(search, pos)) != string::npos) 
	{
		subject.replace(pos, search.length(), replacement);
		pos += replacement.length();
	}
}
