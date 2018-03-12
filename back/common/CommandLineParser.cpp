#include "CommandLineParser.h"

#include <boost/filesystem/operations.hpp>
#include <string>
#include <iostream>

#include "util.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

CommandLineParser::CommandLineParser()
{
	m_commands.add_options()
		("help,h", "output help message")
		("verbose,v", po::value<bool>(&m_bVerbose), "run in verbose mode");
}

CommandLineParser::CommandLineParser(boost::program_options::options_description& additionalOptions)
{
	m_commands.add(additionalOptions);
	m_commands.add_options()
		("help,h", "output help message")
		("verbose,v", po::value<bool>(&m_bVerbose), "run in verbose mode");
}

void CommandLineParser::parseCommandline(int numArguments, char** arguments)
{
	po::store(po::parse_command_line(numArguments, arguments, m_commands), m_optionsMap);
	po::notify(m_optionsMap);
	if (m_optionsMap.count("help")) 
	{
		std::cerr << m_commands << std::endl;
		exit(-1);
	}

	// Positional options without leading letter identifiers
	// #1: input file, usually FuzzTree XML
	// #2: output path for result documents
	// #3: working directory for temporary files
	// #4: path to logfile

	else if (numArguments < 4)
	{
		std::cerr << "Faulty command line options. Use [program_name] [inputfile] [outputfile] [workingdirectory] [logfile, optional]" << std::endl;
		exit(-1);
	}
	std::string outFile, inFile, workingDirectory, logFile;
	inFile				= arguments[1];
	outFile				= arguments[2];
	workingDirectory	= arguments[3] + util::slash;

	m_outFilePath	= fs::path(outFile.c_str());
	m_inFilePath	= fs::path(inFile.c_str());
	m_workingDir	= fs::path(workingDirectory.c_str());

	if (!util::isWritable(outFile))
	{
		std::cerr << "Cannot write to file: " << outFile << std::endl;
		exit(-1);
	}
	else if (!fs::is_regular_file(m_inFilePath))
	{
		std::cerr << "Not a valid file name: " << inFile << std::endl;
		exit(-1);
	}
	else if (!fs::is_directory(m_workingDir) || !util::isWritable(workingDirectory + util::slash + "foo"))
	{
		std::cerr << "Not a writable directory: " << workingDirectory << std::endl;
		exit(-1);
	}

	if (numArguments >= 5)
	{
		logFile = arguments[4];
		if (!util::isWritable(logFile))
		{
			std::cerr << "Log File not writable " << logFile << std::endl;
			exit(-1);
		}
		else m_logFilePath	= fs::path(logFile.c_str());
	}
	int i = 3;
	while (++i < numArguments)
		m_additionalArguments.emplace_back(arguments[i]);
}

const boost::filesystem::path& CommandLineParser::getInputFilePath() const
{
	return m_inFilePath;
}

const boost::filesystem::path& CommandLineParser::getOutputFilePath() const
{
	return m_outFilePath;
}

const boost::filesystem::path& CommandLineParser::getWorkingDirectory() const
{
	return m_workingDir;
}

const std::vector<std::string>& CommandLineParser::getAdditionalArguments() const
{
	return m_additionalArguments;
}

const boost::filesystem::path& CommandLineParser::getLogFilePath() const
{
	return m_logFilePath;
}
