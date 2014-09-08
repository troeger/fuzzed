#include "AbstractModel.h"
#include "OrGate.h"
#include "AndGate.h"
#include "FatalException.h"

#include "Fuzztree.h"
#include "Faulttree.h"

#include <boost/filesystem/operations.hpp>
#include <iostream>

namespace fs = boost::filesystem;
using namespace pugi;

static const char* KIND = "kind";
static const char* DATA = "data";
static const char* KEY = "key";
static const char* ID = "id";
static const char* NODE = "node";
static const char* EDGE = "edge";
static const char* TOPEVENT = "topEvent";
static const char* SOURCE = "source";
static const char* TARGET = "target";

AbstractModel* AbstractModel::loadGraphML(const std::string graphMLFileName)
{
	if (!fs::exists(graphMLFileName) || !fs::is_regular_file(graphMLFileName))
		throw FatalException("Could not read Fuzztree GraphML file");

	{
		xml_document doc;
		if (!doc.load_file(graphMLFileName.c_str()))
			throw FatalException(std::string("Could not load Fuzztree GraphML file: ") + graphMLFileName);
#ifdef DEBUG
		std::cout << "Loaded XML: " << endl;
		doc.print(std::cout);
#endif
		AbstractModel* res = nullptr;

		const std::string modelKind = doc.find_child_by_attribute(DATA, KEY, KIND).value();
		if (modelKind == "fuzztree")
			res = new Fuzztree();
		else if (modelKind == "faulttree")
			res = new Faulttree();
		else throw FatalException(std::string("Could not parse model kind in file: ") + graphMLFileName);

		res->initFromGraphML(doc);
		return res;
	}
}

void AbstractModel::initFromGraphML(const pugi::xml_document& graphMLFile)
{
	std::vector<pugi::xml_node> nodeList;
	for (xml_node node = graphMLFile.child(NODE); node; node = node.next_sibling(NODE))
	{
		if (node.find_child_by_attribute(DATA, KEY, KIND).value() == TOPEVENT)
		{
			if (m_topEvent != nullptr) throw FatalException("Multiple top events detected");
			else m_topEvent = new TopEvent(node.attribute(ID).value());
		}
		else
			nodeList.emplace_back(node);
	}
	
	if (m_topEvent == nullptr) throw FatalException("Could not detect top event");

	std::vector<pugi::xml_node> edgeList;
	for (xml_node edge = graphMLFile.child(EDGE); edge; edge = edge.next_sibling(EDGE))
		edgeList.emplace_back(edge);

	loadTree(nodeList, edgeList);
}

void AbstractModel::loadTree(const std::vector<pugi::xml_node> nodes, const std::vector<pugi::xml_node> edges)
{
	std::string parentID = m_topEvent->getId();
	loadRecursive(nodes, edges, parentID, m_topEvent);
}

void AbstractModel::loadRecursive(
	const std::vector<pugi::xml_node> nodes,
	const std::vector<pugi::xml_node> edges,
	const std::string parentId,
	AbstractNode* parentModelNode)
{
	std::set<std::string> childIds;
	for (const auto e : edges)
	{
		if (e.attribute(SOURCE).value() == parentId)
			childIds.emplace(e.attribute(TARGET).value());
	}

	for (const auto childId : childIds) // recursively descend into child nodes
	{
		AbstractNode* childModelNode = nullptr;
		for (xml_node c : nodes)
		{
			if (c.attribute(ID).value() != childId) continue;
			
			const std::string childType = c.find_child_by_attribute(DATA, KEY, KIND).value();
			if (childType == "basicEvent")
				handleBasicEvent(c, childModelNode);
			else if (childType == "orGate")
				childModelNode = new OrGate(childId);
			else if (childType == "andGate")
				childModelNode = new AndGate(childId);

			assert(childModelNode->getTypeDescriptor() == childType);
			parentModelNode->addChild(childModelNode);
		}
	}
}

const std::string AbstractModel::getId(const pugi::xml_node& node)
{
	return "TODO";
}
