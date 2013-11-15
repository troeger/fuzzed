#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "FuzzTreeTransform.h"

#include <string>
#include <iostream>
#include <fstream>

#include "FatalException.h"
#include "CommandLineParser.h"
#include "FuzzTreeToFaultTree.h"
#include "util.h"
#include "xmlutil.h"
#include "analysisResult.h"


analysisResults::Result analyze(
	const fuzztree::TopEvent* const topEvent,
	std::ofstream* logFileStream,
	analysisResults::AnalysisResults &analysisResults,
	const std::string modelId,
	const int decompositionNumber) 
{
	try
	{
		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(topEvent, decompositionNumber, *logFileStream);
		const auto result = analysis->compute();

		analysisResults::Result r(modelId, util::timeStamp(), true, decompositionNumber);
		r.probability(serialize(result));

		return r;
	}
	catch (const FatalException& e)
	{
		analysisResults::Result r(modelId, util::timeStamp(), false, decompositionNumber);
		r.issue().push_back(e.getIssue().serialized());
		return r;
	}
	catch (const std::exception& e)
	{
		// assert(false);
		// TODO make sure only our exceptions are thrown
		analysisResults::Result r(modelId, util::timeStamp(), false, decompositionNumber);
		commonTypes::Issue i;
		i.message(e.what());
		r.issue().push_back(i);
		return r;	
	}
	catch (...)
	{
		// assert(false);
		// TODO make sure only our exceptions are thrown
		analysisResults::Result r(modelId, util::timeStamp(), false, decompositionNumber);
		commonTypes::Issue i;
		i.message("Unknown Error");
		r.issue().push_back(i);
		return r;	
	}
}



int main(int argc, char** argv)
{
	CommandLineParser parser;
	parser.parseCommandline(argc, argv);
	const auto inFile = parser.getInputFilePath().generic_string();
	const auto outFile = parser.getOutputFilePath().generic_string();
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
		std::ifstream instream(inFile);
		if (!instream.good())
		{
			*logFileStream << "Invalid input file: " << inFile << std::endl;
			return -1;
		}

		analysisResults::AnalysisResults analysisResults;
		
		// please keep this here for debugging
// 		std::istreambuf_iterator<char> eos;
// 		std::string s(std::istreambuf_iterator<char>(instream), eos);
// 		*logFileStream << s;

		FuzzTreeTransform tf(instream, issues);
		instream.close();

		if (!tf.isValid())
		{ // handle faulttree
			std::ifstream is(inFile); // TODO: somehow avoid opening another stream here
			const auto faultTree = faulttree::faultTree(inFile, xml_schema::Flags::dont_validate);
			is.close();

			const auto topEvent = faultTreeToFuzzTree(faultTree->topEvent());
			const auto modelId = faultTree->id();

			const unsigned int decompositionNumber = 
				topEvent->decompositionNumber().present() ? 
				topEvent->decompositionNumber().get() : 
				DEFAULT_DECOMPOSITION_NUMBER;

			analysisResults.result().push_back(
				analyze(topEvent.get(), logFileStream, analysisResults, modelId, decompositionNumber));
		}
		else
		{ // handle fuzztree
			const auto tree = tf.getFuzzTree();
			const auto modelId = tree->id();
			
			const auto topEvent = tree->topEvent();

			const unsigned int decompositionNumber = 
				topEvent.decompositionNumber().present() ? 
				topEvent.decompositionNumber().get() : 
				DEFAULT_DECOMPOSITION_NUMBER;

			for (const auto& t : tf.transform())
			{
				auto topEvent = fuzztree::TopEvent(t.second.topEvent());

				analysisResults::Result r = analyze(&topEvent, logFileStream, analysisResults, modelId, decompositionNumber); 
				r.configuration(serializedConfiguration(t.first));
				analysisResults.result().push_back(r);
			}
		}

		// Log errors
		for (const Issue& issue : issues)
		{
			analysisResults.issue().push_back(issue.serialized());
			*logFileStream << issue.getMessage() << std::endl;
		}

		std::ofstream output(outFile);
		analysisResults::analysisResults(output, analysisResults);
	}

	// This should not happen.
	catch (const xml_schema::Exception& e)
	{
		*logFileStream << "Exception while trying to analyze " << inFile << e.what() << std::endl;
		return -1;
	}
	catch (const std::exception& e)
	{
		*logFileStream << "Exception while trying to analyze " << inFile << e.what() << std::endl;
		return -1;
	}
	catch (...)
	{
		*logFileStream << "Exception while trying to analyze " << inFile << std::endl;
		return -1;
	}
	
	logFileStream->close();
	delete logFileStream;

	return 0;
}
