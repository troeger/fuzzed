#include "FuzzTreeTransform.h"

#include <string>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/program_options.hpp>
#include <iostream>
#include <fstream>

#include "util.h"
#include "CommandLineParser.h"
#include "FatalException.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv)
{
	CommandLineParser parser;
	parser.parseCommandline(argc, argv);
	const auto inFile	= parser.getInputFilePath().generic_string();
	const auto outFile	= parser.getOutputFilePath().generic_string();
	const auto logFile = parser.getLogFilePath().generic_string();

	std::ofstream* logFileStream = new std::ofstream(logFile);
	*logFileStream << "Analysis errors for " << inFile << std::endl;
	if (!logFileStream->good())
	{// create default log file
		logFileStream = new std::ofstream(
			parser.getWorkingDirectory().generic_string() +
			util::slash +
			"errors.txt");	
	}

	std::vector<Issue> issues;
	try
	{
		// do the actual transformation, write all files to dirPath
		std::ifstream instream(inFile);
		if (!instream.good())
		{
			std::cerr << "Invalid input file: " << inFile << std::endl;
			return -1;
		}
		FuzzTreeTransform transform(instream, issues);
		if (!transform.isValid())
		{
			std::cerr << "Could not compute configurations." << std::endl;
			return -1;
		}

		const auto fileName = util::fileNameFromPath(inFile);

		transform.generateConfigurationsFile(outFile);
		return 0;
	}
	catch (const std::exception& e)
	{
		std::cerr << "Exception while trying to configure " << inFile << e.what() << std::endl;
		return -1;
	}
	catch (...)
	{
		std::cerr << "Exception while trying to configure " << inFile << std::endl;
		return -1;
	}
}