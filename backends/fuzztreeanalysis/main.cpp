#include "InstanceAnalysisTask.h"

#include <fstream>

int main()
{
	static const std::string testfile = "C:\\dev\\fuzztrees\\simulation\\testdata\\faultTrees\\single_and_gate.fuzztree";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;

	const auto t = faulttree::faultTree(file, xml_schema::Flags::dont_validate);
	InstanceAnalysisTask analysis(t->topEvent(), 10);
	const auto foo = analysis.compute();
}