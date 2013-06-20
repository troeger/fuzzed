#include "TreeHelpers.h"

faulttree::BasicEvent treeHelpers::copyBasicEvent(const fuzztree::BasicEvent& be)
{
	return faulttree::BasicEvent(be.id(), copyProbability(be.probability()));
}

faulttree::Gate treeHelpers::copyGate(const fuzztree::Gate& gate)
{
	faulttree::Gate res(gate.id());
	return res;
}

faulttree::Probability treeHelpers::copyProbability(const fuzztree::Probability& prob)
{
	const fuzztree::CrispProbability* crisp = dynamic_cast<const fuzztree::CrispProbability*>(&prob);
	if (crisp) return faulttree::CrispProbability(crisp->value());

	else
	{
		const fuzztree::DecomposedFuzzyProbability* fuzzy = 
			dynamic_cast<const fuzztree::DecomposedFuzzyProbability*>(&prob);
		return faulttree::CrispProbability(0); // TODO
	}
}

faulttree::TopEvent treeHelpers::copyTopEvent(const fuzztree::TopEvent& topEvent)
{
	return faulttree::TopEvent(topEvent.id());
}

