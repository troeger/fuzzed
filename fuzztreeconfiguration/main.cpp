#include "FuzzTreeTransform.h"

int main(int argc, char **argv)
{
	if (argc < 2)
	{
		std::cout << "Too few arguments. Please specify a filename.";
		return -1;
	}
	const std::string fileName(argv[1]);
	auto fttransform = FuzzTreeTransform(fileName);

	for (auto tree : fttransform.transform())
	{
	}
}