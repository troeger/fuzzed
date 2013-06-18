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

	FaultTreeNode(const std::string& ID, const std::string& name = "");
	virtual FaultTreeNode* clone() const = 0; // virtual deep copying

	virtual ~FaultTreeNode();

	// override to enforce assertions
	virtual void addChild(FaultTreeNode* child);
	
	virtual bool addChildBelow(const std::string& ID, FaultTreeNode* child);

	NodeList::const_iterator getChildrenBegin() const	{ return m_children.begin(); };
	NodeList::const_iterator getChildrenEnd()	const	{ return m_children.end(); };

	FaultTreeNode* getChildById(const std::string& ID);

	int getNumChildren() const { return m_children.size(); };

	virtual bool isValid() const { return m_children.size() > 0; };
	const std::string getId() const { return m_id; };
	
	virtual int getCost() const;

	// returns ID of the "top level" place
	virtual int serialize(boost::shared_ptr<PNDocument> doc) const = 0;
	virtual std::string serializeAsFormula(boost::shared_ptr<PNDocument> doc) const = 0;
	
	std::pair<int /*placeID*/,int /*spareActivationTransition*/> serializeAsColdSpare(boost::shared_ptr<PNDocument> doc) const;
	
	// uses RTTI
	virtual void print(std::ostream& stream, int indentLevel=0) const;

	const FaultTreeNode* getRoot() const;
	const FaultTreeNode* getParent() const { return m_parent; };
	virtual void setParent(FaultTreeNode* parent) { m_parent = parent; };

protected:
	virtual std::string description() const;

	NodeList m_children;
	FaultTreeNode* m_parent;

	std::string m_id;
	int m_cost;

	std::string m_name;
};