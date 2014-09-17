#include "Model.h"
#include "FuzzTreeToFaultTree.h"
#include <iostream>

int main()
{
	// Test GraphML import
	const std::string FILENAME = "test.graphml";
	Model m = Model(FILENAME);
}