#pragma once
#include "Node.h"
#include <fstream>
#include <pugixml.hpp>

namespace modeltype
{
    const std::string FUZZTREE   = "fuzztree";
    const std::string FAULTTREE  = "faulttree";
}

class Model
{
public:
    Model(const std::string graphMLFile);

private:
    void loadTree(const std::vector<pugi::xml_node>& nodes, const std::vector<pugi::xml_node>& edges);
    void loadRecursive(
        const std::vector<pugi::xml_node> nodes,
        const std::vector<pugi::xml_node> edges,
        const std::string parentId,
        Node* parentModelNode);

    static void printTreeRecursive(const Node* node, unsigned int indent);

    Model(std::string type, std::string id, std::string name)
        : m_type(type), m_id(id), m_name(name), m_topEvent(nullptr)
    {};

    std::string m_id;
    std::string m_type;

    std::string m_name;

    /**
     * Fuzztree members
     */
    unsigned int m_decompositionNumber;

    Node* m_topEvent;
};