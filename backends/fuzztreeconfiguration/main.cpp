#include <string>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/program_options.hpp>
#include <iostream>
#include <fstream>

#include "util.h"
#include "xmlutil.h"
#include "CommandLineParser.h"
#include "FatalException.h"
#include "FuzzTreeToFaultTree.h"
#include "resultxml.h"
#include "Result.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

int main(int argc, char **argv)
{
	CommandLineParser parser;
	parser.parseCommandline(argc, argv);
	const auto inFile	= parser.getInputFilePath().generic_string();
	const auto outFile	= parser.getOutputFilePath().generic_string();
	const auto logFile	= parser.getLogFilePath().generic_string();

	std::ofstream* logFileStream = new std::ofstream(logFile);
	*logFileStream << "Configuration errors for " << inFile << std::endl;
	if (!logFileStream->good())
	{// create default log file
		logFileStream = new std::ofstream(
			parser.getWorkingDirectory().generic_string() +
			util::slash +
			"errors.txt");
	}

	Model m(inFile);
	ResultsXML xml;
	const std::string modelId = m.getId();

	std::ifstream instream(inFile);
	if (!instream.good())
	{
		*logFileStream << "Invalid input file: " << inFile << std::endl;
		return -1;
	}

	std::set<Issue> issues; // issues at fuzztree level
	if (m.getType() == modeltype::FUZZTREE)
	{
		FuzzTreeToFaultTree transform(&m);
		const auto configs = transform.generateConfigurations();
		auto output = std::ofstream(outFile);
		xml.generate(configs, issues, output);
	}
	else
	{
		issues.insert(Issue::fatalIssue("Not a FuzzTree model"));
	}
	

	logFileStream->close();
	delete logFileStream;

	return 0;
}