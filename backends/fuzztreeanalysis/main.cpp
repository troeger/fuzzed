#include "InstanceAnalysisTask.h"
#include <fstream>
#include <iostream>

int main()
{
	static const std::string testfile = "C:\\dev\\fuzztrees\\backends\\simulation\\testdata\\mixed.fuzztree";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;
	try
	{
		const auto t = fuzztree::fuzzTree(file, xml_schema::Flags::dont_validate);
		InstanceAnalysisTask analysis(t->topEvent(), 10);
		const auto foo = analysis.compute();
	}
	catch (const std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}
	return 0;
}