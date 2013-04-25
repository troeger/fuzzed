#pragma once

#include <boost/shared_ptr.hpp>
#include <vector>
#include <ostream>

#include "pugixml.hpp"

class PNDocument;

class FaultTreeNode
{
public:
	typedef std::vector<FaultTreeNode*> NodeList;

	FaultTreeNode(int ID, const std::string& name = "");
	virtual FaultTreeNode* clone() const = 0; // virtual deep copying

	virtual ~FaultTreeNode();

	// override to enforce assertions
	virtual void addChild(FaultTreeNode* child);
	
	virtual bool addChildBelow(int id, FaultTreeNode* child);

	NodeList::const_iterator getChildrenBegin() const	{ return m_children.begin(); };
	NodeList::const_iterator getChildrenEnd()	const	{ return m_children.end(); };

	FaultTreeNode* getChildById(int id);

	int getNumChildren() const { return m_children.size(); };

	virtual bool isValid() const { return m_children.size() > 0; };

	virtual long double getValue() const = 0;
	int getId() const { return m_id; };
	
	virtual int getCost() const;

	// returns ID of the "top level" place
	virtual int serialize(boost::shared_ptr<PNDocument> doc) const = 0;
	virtual int serialize(PNDocument* doc);
	
	// uses RTTI
	virtual void print(std::ostream& stream, int indentLevel=0) const;

	const FaultTreeNode* getRoot() const;
	FaultTreeNode* getParent() const { return m_parent; };
	virtual void setParent(FaultTreeNode* parent) { m_parent = parent; };

protected:
	virtual std::string description() const;

	NodeList m_children;
	FaultTreeNode* m_parent;

	int m_id;
	int m_cost;

	std::string m_name;
};