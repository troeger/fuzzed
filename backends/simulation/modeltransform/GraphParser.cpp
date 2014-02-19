#include "GraphParser.h"
#include <cassert>
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
	catch (...)
	{
		if (logfile)
			*logfile << "Unknown error during simulation";
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
	
	loadPropertySpecs(dp, g);

	read_graphml(m_file, g, dp);
	write_graphml(std::cout, g, dp);

	FaultTreeNode::Ptr ft = nullptr;
	for (auto vp = vertices(g); vp.first != vp.second; ++vp.first)
	{
		const auto i = *vp.first;
		const auto kind = get(&FTNode::kind, g, i);
		const auto ID = get(vertex_index, g, i);

		if (kind == "TopEvent")
		{ // recursively build tree, starting from Top Event
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
	const std::string ID = "foo";//TODO: get(vertex_name, g, i);

	FaultTreeNode::Ptr newNode;
	if (kind == "BasicEvent")
		newNode = FaultTreeNode::Ptr(new BasicEvent(ID, parseProbability(get(&FTNode::probability, g, i))));

	else if (kind == "And")
		newNode = FaultTreeNode::Ptr(new ANDGate(ID));
		
	else if (kind == "Or")
		newNode = FaultTreeNode::Ptr(new ORGate(ID));

	else if (kind == "VotingOr")
		newNode = FaultTreeNode::Ptr(new VotingORGate(ID, get(&FTNode::k, g, i)));
	
	else if (kind == "FDEP")
	{
		// const FaultTreeNode::Ptr ag(new FDEPGate(ID, trigger, dependentEvents));
	}
	else if (kind == "Spare")
	{
		const std::string primary = ""; // TODO
		newNode = FaultTreeNode::Ptr(new SpareGate(ID, primary, get(&FTNode::dormancyFactor, g, i)));
	}
	else if (kind == "PAND")
	{

	}
	else if (kind == "ImmediateEvent")
	{

	}
	else if (kind == "BasicEventSet")
	{// TODO: assert that parent is a gate
		const long cardinality = get(&FTNode::cardinality, g, i);
		const double probability = parseProbability(get(&FTNode::probability, g, i));
		for (long i = 0; i < cardinality; ++i)
		{
			ft->addChild(FaultTreeNode::Ptr(new BasicEvent(ID + util::toString(i), probability)));
		}
	}
	else if (kind == "UndevelopedEvent")
		throw std::runtime_error("Cannot simulate trees with undeveloped events!");
	
	else if (kind == "HouseEvent")
		newNode = FaultTreeNode::Ptr(new BasicEvent(ID, 0.0));
	
	if (newNode)
		ft->addChild(newNode);
	else
		newNode = ft; // Top or Intermediate Events

	for (auto op = out_edges(i, g); op.first != op.second; ++op.first)
	{
		const auto ei = *op.first;
		
		const auto targetIndex = target(ei, g);
		scanTree(g, targetIndex, newNode);
	}
}

double GraphParser::parseProbability(const std::string crypticGraphMLRubbish)
{
	std::istringstream i(crypticGraphMLRubbish);
	double x;
	if (!(i >> x))
		return 0.0;
	return x;
}

void GraphParser::loadPropertySpecs(boost::dynamic_properties &dp, BoostGraphType& g)
{
	static const std::string vk = "kind";
	static const std::string prob = "probability";
	static const std::string k = "k";
	static const std::string df = "dormancyFactor";
	static const std::string card = "cardinality";

	dp.property(vk,		get(&FTNode::kind,			g));
	dp.property(prob,	get(&FTNode::probability,	g));
	dp.property(k,		get(&FTNode::k,				g));
	dp.property(df,		get(&FTNode::dormancyFactor,g));
	dp.property(card,	get(&FTNode::cardinality,	g));
}
