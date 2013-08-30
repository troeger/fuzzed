#pragma once

#include <boost/shared_ptr.hpp>
#include <vector>
#include <ostream>

#include "pugixml.hpp"
#include "serialization/TNDocument.h"

class FaultTreeNode
{
public:
	typedef std::shared_ptr<FaultTreeNode> Ptr;
	typedef std::vector<FaultTreeNode::Ptr> NodeList;

	/************************************************************************/
	/* object creation                                                      */
	/************************************************************************/
	virtual FaultTreeNode::Ptr clone() const = 0; // virtual deep copying
	virtual ~FaultTreeNode();
	
	FaultTreeNode(const std::string& ID, const std::string& name = "");

	/************************************************************************/
	/* tree manipulation                                                    */
	/************************************************************************/
	virtual void addChild(FaultTreeNode::Ptr child);
	virtual bool addChildBelow(const std::string& ID, FaultTreeNode::Ptr child);

	virtual void setParent(FaultTreeNode* parent) { m_parent = parent; }

	NodeList::const_iterator getChildrenBegin() const { return m_children.begin(); }
	NodeList::const_iterator getChildrenEnd()	const { return m_children.end(); }


	/************************************************************************/
	/* data access                                                          */
	/************************************************************************/
	FaultTreeNode::Ptr getChildById(const std::string& ID);
	const FaultTreeNode::Ptr getChildById(const std::string& ID) const; // TODO copy-pasted just to enforce const-ness

	int getNumChildren() const { return m_children.size(); };

	virtual bool isValid() const { return m_children.size() > 0; };
	const std::string& getId() const { return m_id; };
	
	virtual int getCost() const;

	const FaultTreeNode* getRoot() const;
	const FaultTreeNode* getParent() const;;
	
	/************************************************************************/
	/* serialization                                                        */
	/************************************************************************/

	// returns ID of the "top level" place
	virtual int serializePTNet(std::shared_ptr<PNDocument> doc) const = 0;
	virtual int serializeTimeNet(std::shared_ptr<TNDocument> doc) const;

	virtual std::string serializeAsFormula(std::shared_ptr<PNDocument> doc) const = 0;

	std::pair<int /*placeID*/,int /*spareActivationTransition*/> 
		serializeAsColdSpare(std::shared_ptr<PNDocument> doc) const;

	// uses RTTI
	virtual void print(std::ostream& stream, int indentLevel=0) const;

protected:
	void markDynamic(); 

	virtual std::string description() const;

	NodeList m_children;
	FaultTreeNode* m_parent;

	std::string m_id;
	int m_cost;

	std::string m_name;

	bool m_bDynamic;
	bool m_bStaticSubTree;
};