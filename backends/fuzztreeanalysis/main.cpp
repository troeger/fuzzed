#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include <fstream>
#include <iostream>

int main()
{
	const std::string testfile = "C:\\dev\\fuzztrees\\backends\\fuzztreeanalysis\\testdata\\EWDC2013.fuzztree"; // "C:\\dev\\fuzztrees\\backends\\simulation\\testdata\\mixed.fuzztree";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;
	try
	{
		auto t = fuzztree::fuzzTree(file, xml_schema::Flags::dont_validate);
		file.close();

		auto topEvent = fuzztree::TopEvent(t->topEvent());
		
		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, 10);
		const auto foo = analysis->compute();
	}
	catch (const std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

	return 0;
}