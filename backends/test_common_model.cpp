#include "Model.h"
#include "FuzzTreeToFaultTree.h"
#include <iostream>

int main()
{
	// Test GraphML import
	const std::string FILENAME = "test.graphml";
	Model m = Model(FILENAME);

    FuzzTreeToFaultTree transform(&m);
    for (const auto& c : transform.generateConfigurations())
    {
        Model faulttree = transform.faultTreeFromConfiguration(c);
        Model::printTreeRecursive(faulttree.getTopEvent(), 0);
    }
}