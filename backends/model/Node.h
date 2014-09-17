#pragma once
#include <string>
#include <vector>
#include <cassert>

// TODO
typedef double Probability;

namespace nodetype
{
    const std::string AND   = "andGate";
    const std::string OR    = "orGate";

    const std::string BASICEVENT    = "basicEvent";
    const std::string TOPEVENT      = "topEvent";

    const std::string INTERMEDIATEEVENT = "intermediateEvent";
    const std::string UNDEVELOPEDEVENT  = "undevelopedEvent";
}


class Node
{
public:
    friend class Model;

    typedef std::vector<Node> ChildList;

    Node(const std::string type, const std::string id, const std::string name="") :
        m_type(type), m_id(id), m_name(name) {};

    void addChild(const Node c) { m_children.emplace_back(c); }
    const ChildList& getChildren() const { return m_children; }

    const std::string& getType() const   { return m_type; }
    const std::string& getId()   const   { return m_id; }
    const std::string& getName() const   { return m_name; }

    const bool& isOptional()        const { return m_isOptional; }
    const unsigned int& getCost()   const { return m_cost; }

    /**
     * Utility functions
     */
    bool isEvent() const;
    bool isGate() const;
    bool isLeaf() const;
    bool isVariationPoint() const;

    const Probability& getProbability() const { assert(m_type == nodetype::BASICEVENT); return m_probability; }

    std::string print() const { return std::string("- ") + m_type + " ID: " + m_id + " " + m_name; };

private:
    ChildList& getChildren() { return m_children; } // Access only by Model

    std::vector<Node> m_children;

    std::string m_id;
    std::string m_name;
    
    std::string m_type;

    bool m_isOptional;

    unsigned int m_cost;

    /**
     * Basic Event members
     */
    Probability m_probability;
};