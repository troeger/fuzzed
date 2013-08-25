#include "FuzzTreeTransform.h"
#include "FuzzTreeConfigClient.h"
#include "beanstalkdconfig.h"
#include "PrintVisitor.h"

#include <fstream>

int main(int argc, char **argv)
{
	static const std::string testfile = "C:\dev\fuzztrees\simulation\testdata\faultTrees";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;

	auto topevent = faulttree::faultTree(file, xml_schema::Flags::dont_validate)->topEvent();

	PrintVisitor pv;
	pv.visit(&topevent);

// 	FuzzTreeConfigClient client(BEANSTALK_SERVER, BEANSTALK_PORT);
// 	client.run();
}