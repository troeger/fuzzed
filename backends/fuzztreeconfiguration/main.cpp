#include "FuzzTreeTransform.h"

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

#include "configurationResult.h"

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
		logFileStream = new std::ofstream(logFile);	// TODO: wtf this is the same line as above? retry?
	}

	std::ifstream instream(inFile);
	if (!instream.good())
	{
		*logFileStream << "Invalid input file: " << inFile << std::endl;
		return -1;
	}

	std::set<Issue> issues; // issues at fuzztree level
	FuzzTreeTransform tf(instream, issues);
	instream.close();

	try
	{
		configurationResults::ConfigurationResults configurationResults;

		if (!tf.isValid())
		{ // only fuzztrees should be configured 
			issues.insert(Issue::fatalIssue("Could not configure the model. Did you try to configure a fault tree?"));
		}
		else
		{ // handle fuzztree
			const auto modelId = tf.getFuzzTree()->id();
			for (const auto& t : tf.transform())
			{
				configurationResults::Result r(modelId, util::timeStamp(), true); 
				r.configuration(serializedConfiguration(t.first));
				configurationResults.result().push_back(r);
			}
		}

		// Log errors
		for (const Issue& issue : issues)
		{
			configurationResults.issue().push_back(issue.serialized());
			*logFileStream << issue.getMessage() << std::endl;
		}

		std::ofstream output(outFile);
		configurationResults::configurationResults(output, configurationResults);
	}

	// This should not happen.
	catch (const std::exception& e)
	{
		*logFileStream << "Exception while trying to configure " << inFile << e.what() << std::endl;
		fuzztree::fuzzTree(*logFileStream, *(tf.getFuzzTree()));

		return -1;
	}
	catch (...)
	{
		*logFileStream << "Exception while trying to configure " << inFile << std::endl;
		return -1;
	}

	logFileStream->close();
	delete logFileStream;

	return 0;
}