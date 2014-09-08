#include "Fuzztree.h"
#include <iostream>

int main()
{
	// Test GraphML import
	const std::string FILENAME = "test.graphml";
	
	const AbstractModel* model = AbstractModel::loadGraphML(FILENAME);
	if (model->getTypeDescriptor() == "fuzztree")
		std::cout << "Loaded fuzztree.";
	else if (model->getTypeDescriptor() == "faulttree")
		std::cout << "Loaded faulttree";
}