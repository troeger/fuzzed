#include "FuzzTreeTransform.h"
#include "FuzzTreeConfigClient.h"
#include "beanstalkdconfig.h"

int main(int argc, char **argv)
{
	
	
	FuzzTreeConfigClient client("foo", BEANSTALK_SERVER, BEANSTALK_PORT);
	client.run();


// 	if (argc < 2)
// 	{
// 		std::cout << "Too few arguments. Please specify a filename.";
// 		return -1;
// 	}
// 	const std::string fileName(argv[1]);
// 	auto fttransform = FuzzTreeTransform(fileName);
// 
// 	for (auto tree : fttransform.transform())
// 	{
// 	}
}