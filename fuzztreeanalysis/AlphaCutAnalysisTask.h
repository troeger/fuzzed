#pragma once
#include "Visitor.h"

typedef double AlphaCutAnalysisResult;

class AlphaCutAnalysisTask : public faulttree::Visitor
{
public:
	AlphaCutAnalysisTask(faulttree::TopEvent& topEvent, const double& alpha);

	void run();

	virtual void visit(faulttree::Node&);
	virtual void visit(faulttree::ChildNode&);

	virtual void visit(faulttree::BasicEvent&);
	virtual void visit(faulttree::TopEvent&);
	virtual void visit(faulttree::HouseEvent&);
	virtual void visit(faulttree::UndevelopedEvent&);
	virtual void visit(faulttree::IntermediateEvent&);

	virtual void visit(faulttree::Gate&);
	virtual void visit(faulttree::DynamicGate&);

	virtual void visit(faulttree::And&);
	virtual void visit(faulttree::Or&);
	virtual void visit(faulttree::Xor&);
	virtual void visit(faulttree::VotingOr&);

	virtual void visit(faulttree::Spare&);
	virtual void visit(faulttree::FDEP&);
	virtual void visit(faulttree::PriorityAnd&);
	virtual void visit(faulttree::Sequence&);

protected:
	const double m_alpha;
	faulttree::TopEvent& m_tree;
};