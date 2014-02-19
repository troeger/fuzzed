#pragma once

#include <fstream>
#include <string>

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphml.hpp>

#include "FaultTreeNode.h"

// Vertex properties
struct FTNode
{
	std::string kind;
	std::string probability;
	long k;
	long cardinality;
	double dormancyFactor; 
};

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::directedS, FTNode> BoostGraphType;

class GraphParser
{
public:
	static FaultTreeNode::Ptr fromGraphML(const std::string& fileName, std::ofstream* logfile);

private:
	GraphParser(const std::string& fileName);
	FaultTreeNode::Ptr parse();

	static void loadPropertySpecs(boost::dynamic_properties& dp, BoostGraphType& g);
	static void scanTree(BoostGraphType& graph, int index, FaultTreeNode::Ptr ftn);

	static double parseProbability(const std::string crypticGraphMLRubbish);

	std::ifstream m_file;
};
