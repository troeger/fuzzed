#include "Model.h"
#include "FuzzTreeToFaultTree.h"
#include <iostream>

int main()
{
	// Test GraphML import
	const std::string FILENAME = "test.graphml";
	Model m = Model(FILENAME);

    FuzzTreeToFaultTree transform(&m);
	const auto res = transform.generateConfigurations();
    for (const auto& c : transform.generateConfigurations())
    {
        Model faulttree = transform.faultTreeFromConfiguration(c);
		assert(faulttree.getTopEvent() != nullptr);
        Model::printTreeRecursive(faulttree.getTopEvent(), 0);
    }
}