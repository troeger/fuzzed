#pragma once
#include "fuzztree.h"
#include "VerificationResult.h"

/************************************************************************/
/* Verifies a fuzztree													*/
/************************************************************************/

class VerificationTask
{
public:
	VerificationTask(fuzztree::TopEvent& tree);
	VerificationResult compute();
	
protected:
	void computeRecursive(VerificationResult& res, const fuzztree::ChildNode& node);

	fuzztree::TopEvent& m_tree;
};