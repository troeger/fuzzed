#include "GraphParser.h"
#include <cassert>
#include <boost/graph/property_iter_range.hpp>
#include <boost/graph/graphml.hpp>

#include "FaultTreeIncludes.h"
#include "util.h"

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
	
	BoostGraphType g;
	dynamic_properties dp ;
	
	const std::string vk = "kind";
	const std::string prob = "probability";
	const std::string k = "k";
	const std::string df = "dormancyFactor";
	const std::string card = "cardinality";
	dp.property(vk,		get(&FTNode::kind,			g));
	dp.property(prob,	get(&FTNode::probability,	g));
	dp.property(k,		get(&FTNode::k,				g));
	dp.property(df,		get(&FTNode::dormancyFactor,g));
	dp.property(card,	get(&FTNode::cardinality,	g));
	
	read_graphml(m_file, g, dp);
	write_graphml(std::cout, g, dp);

	FaultTreeNode::Ptr ft = nullptr;
	for (auto vp = vertices(g); vp.first != vp.second; ++vp.first)
	{
		const auto i = *vp.first;
		const auto kind = get(&FTNode::kind, g, i);
		const auto ID = get(vertex_index, g, i);

		std::cout 
			<< kind << " "
			<< get(&FTNode::probability, g, i) << " "
			<< "index " << ID << std::endl;

		if (kind == "TopEvent")
		{ // recursively build tree
			ft.reset(new TopLevelEvent(util::toString((int)ID)));
			scanTree(g, i, ft);
			break;
		} else continue;
	}

	ft->print(std::cout);
	return ft;
}

void GraphParser::scanTree(BoostGraphType& g, int i, FaultTreeNode::Ptr ft)
{
	using namespace boost;

	const auto kind = get(&FTNode::kind, g, i);
	const std::string ID = "foo";//get(vertex_name, g, i);

	if (kind == "BasicEvent")
	{
		const FaultTreeNode::Ptr be(new BasicEvent(ID, parseProbability(get(&FTNode::probability, g, i))));
		ft->addChild(be);
		return; // FDEP?!
	} 
	else if (kind == "And")
	{
		const FaultTreeNode::Ptr ag(new ANDGate(ID));
		ft->addChild(ag);
		ft = ag;
	}

	for (auto op = out_edges(i, g); op.first != op.second; ++op.first)
	{
		const auto ei = *op.first;
		std::cout << "---" << ei << std::endl;

		const auto targetIndex = target(ei, g);
		scanTree(g, targetIndex, ft);
	}
}

double GraphParser::parseProbability(const std::string crypticGraphMLRubbish)
{
	std::istringstream i(crypticGraphMLRubbish);
	double x;
	if (!(i >> x))
		return 0;
	return x;
}
