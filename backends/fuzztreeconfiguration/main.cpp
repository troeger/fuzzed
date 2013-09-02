#include "FuzzTreeTransform.h"
#include "FuzzTreeConfigClient.h"
#include "beanstalkdconfig.h"
// #include "PrintVisitor.h"
#include "TreeHelpers.h"

#include <fstream>

int main(int argc, char **argv)
{
	static const std::string testfile = "C:\\dev\\fuzztrees\\simulation\\testdata\\configurations\\optional.fuzztree";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;

	FuzzTreeTransform t(file);
	for (auto result : t.transform())
	{
		// treeHelpers::printTree(result.topEvent(), 0);
// 		PrintVisitor pv;
// 		pv.visit(result.topEvent());
	}
// 	FuzzTreeConfigClient client(BEANSTALK_SERVER, BEANSTALK_PORT);
// 	client.run();
}