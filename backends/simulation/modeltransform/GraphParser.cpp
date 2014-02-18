#include "GraphParser.h"
#include <cassert>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/property_iter_range.hpp>
#include <boost/graph/graphml.hpp>

FaultTreeNode::Ptr GraphParser::fromGraphML(const std::string& fileName, std::ofstream* logfile)
{
	assert(!fileName.empty());
	try
	{
		GraphParser gp(fileName);
		return gp.parse();
	}
	catch (std::exception& e)
	{
		if (logfile)
			*logfile << e.what();
	}
}

GraphParser::GraphParser(const std::string& fileName)
	: m_file(fileName, std::ifstream::in)
{}

FaultTreeNode::Ptr GraphParser::parse()
{
	if (!m_file.is_open())
		throw std::runtime_error("Could not load GraphML.");

	using namespace boost;

	// Vertex properties
	struct FTNode {
		std::string kind;
		std::string probability;
	};

	typedef adjacency_list<vecS, vecS, directedS, FTNode> BoostGraphType;
	typedef dynamic_properties BoostDynamicProperties;

	BoostGraphType g;
	BoostDynamicProperties dp ;
	
	const std::string vk = "kind";
	const std::string prob = "probability";
	dp.property(vk,		get(&FTNode::kind,			g));
	dp.property(prob,	get(&FTNode::probability,	g));
	
	read_graphml(m_file, g, dp);

	for (auto vp = vertices(g); vp.first != vp.second; ++vp.first)
	{
		const auto i = *vp.first;
		std::cout 
			<< get(&FTNode::kind, g, i) << "' "
			<< get(&FTNode::probability, g, i) << "' "
			<< "index '" << get(vertex_index, g, i) << std::endl;
	}

	return FaultTreeNode::Ptr();
}
