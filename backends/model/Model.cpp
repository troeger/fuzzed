#include "Model.h"
#include "FatalException.h"

#include <boost/filesystem/operations.hpp>
#include <iostream>
#include <set>

namespace fs = boost::filesystem;
using namespace pugi;

static const char* KIND = "kind";
static const char* DATA = "data";
static const char* KEY = "key";
static const char* ID = "id";
static const char* NODE = "node";
static const char* EDGE = "edge";
static const char* SOURCE = "source";
static const char* TARGET = "target";
static const char* NAME = "name";
static const char* OPTIONAL = "optional";

#define GET_STRING_VALUE_BY_ATTR(NODE, CHILD, ATTR, VAL) (std::string(NODE.find_child_by_attribute(CHILD, ATTR, VAL).text().as_string()))
#define GET_BOOL_VALUE_BY_ATTR(NODE, CHILD, ATTR, VAL) (NODE.find_child_by_attribute(CHILD, ATTR, VAL).text().as_bool())

Model::Model(const std::string graphMLFileName)
{
    if (!fs::exists(graphMLFileName) || !fs::is_regular_file(graphMLFileName))
        throw FatalException("Could not read Fuzztree GraphML file");

    /**
     * Try to load the file...
     */
    xml_document doc;
    if (!doc.load_file(graphMLFileName.c_str()))
        throw FatalException(std::string("Could not load Fuzztree GraphML file: ") + graphMLFileName);

#ifdef DEBUG
    std::cout << "Loaded XML: " << endl;
    doc.print(std::cout);
#endif
    const xml_node graph = doc.child("graphml").child("graph");
    //graph.print(std::cout);
    //graph.find_child_by_attribute(DATA, KEY, KIND).print(std::cout);
    
    m_type = GET_STRING_VALUE_BY_ATTR(graph, DATA, KEY, KIND);

    if (m_type != modeltype::FUZZTREE && m_type != modeltype::FAULTTREE)
        throw FatalException(std::string("Could not parse model kind in file: ") + m_type);
    
    /**
     * Load the nodes...
     */
    m_topEvent = nullptr;

    std::vector<pugi::xml_node> nodeList;
    for (xml_node node = graph.child(NODE); node; node = node.next_sibling(NODE))
    {
        node.print(std::cout);
        if (GET_STRING_VALUE_BY_ATTR(node, DATA, KEY, KIND) == nodetype::TOPEVENT)
        {
            if (m_topEvent != nullptr)
                throw FatalException("Multiple top events detected");
            else
                m_topEvent = new Node(nodetype::TOPEVENT, node.attribute(ID).value());
        }
        else
            nodeList.emplace_back(node);
    }
    
    if (m_topEvent == nullptr) throw FatalException("Could not detect top event");

    /**
     * Load the edges...
     */
    std::vector<pugi::xml_node> edgeList;
    for (xml_node edge = graph.child(EDGE); edge; edge = edge.next_sibling(EDGE))
        edgeList.emplace_back(edge);

    if (nodeList.empty() || edgeList.empty()) throw FatalException("Could not load nodes or edges");

    loadTree(nodeList, edgeList);
}

void Model::loadTree(const std::vector<pugi::xml_node>& nodes, const std::vector<pugi::xml_node>& edges)
{
    loadRecursive(nodes, edges, m_topEvent->getId(), m_topEvent);
    printTreeRecursive(m_topEvent, 0);
}

void Model::loadRecursive(
    const std::vector<pugi::xml_node> nodes,
    const std::vector<pugi::xml_node> edges,
    const std::string parentId,
    Node* parentModelNode)
{
    std::set<std::string> childIds;
    for (const auto e : edges)
    { // Try to find all children for this parent.
        if (e.attribute(SOURCE).value() == parentId)
            childIds.emplace(e.attribute(TARGET).value());
    }

    for (const auto childId : childIds) // recursively descend into child nodes
    {
        Node* childModelNode = nullptr;
        for (const xml_node& c : nodes)
        {
            const std::string cid = c.attribute(ID).value();
            if (cid != childId) continue;
            
            const std::string childType = GET_STRING_VALUE_BY_ATTR(c, DATA, KEY, KIND);
            parentModelNode->addChild(Node(
                childType,
                cid,
                GET_BOOL_VALUE_BY_ATTR(c, DATA, KEY, OPTIONAL),
                GET_STRING_VALUE_BY_ATTR(c, DATA, KEY, NAME)));
            {
                if (childType == nodetype::BASICEVENT)
                { // determine probability

                }
            }

            loadRecursive(nodes, edges, cid, &parentModelNode->getChildren().back());
        }
    }
}

void Model::printTreeRecursive(const Node* node, unsigned int indent)
{
    for (unsigned int i = 0; i < indent; ++i)
        std::cout << " ";
    std::cout << node->print() << std::endl;

    for (const auto c : node->getChildren())
        printTreeRecursive(&c, indent+4);
}