#pragma once

#include "faulttree.h"
#include "fuzztree.h"

namespace treeHelpers
{

	/************************************************************************/
	/* Transforming Fuzztree nodes to Faulttree nodes with same information */
	/* this can also be done via xsd --custom-type (see CMakeLists.txt)     */
	/************************************************************************/

	faulttree::BasicEvent	copyBasicEvent(const fuzztree::BasicEvent& be);
	faulttree::Gate			copyGate(const fuzztree::Gate& gate);
	faulttree::Probability	copyProbability(const fuzztree::Probability& prob);
	faulttree::TopEvent		copyTopEvent(const fuzztree::TopEvent& topEvent);
}