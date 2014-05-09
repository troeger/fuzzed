#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "FuzzTreeTransform.h"

#include <string>
#include <iostream>
#include <fstream>

#include "FatalException.h"
#include "CommandLineParser.h"
#include "FaultTreeToFuzzTree.h"
#include "util.h"
#include "xmlutil.h"
#include "backendResult.h"


void analyze(
	backendResults::AnalysisResult& r,
	const fuzztree::TopEvent* const topEvent,
	std::ofstream* logFileStream,
	unsigned int decompositionNumber) 
{
	try
	{
		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(topEvent, decompositionNumber, *logFileStream);
		const auto result = analysis->compute();

		r.probability(serialize(result));
	}
	catch (const FatalException& e)
	{
		r.validResult(false);
		r.issue().push_back(e.getIssue().serialized());
	}
	catch (const std::exception& e)
	{
		r.validResult(false);
		commonTypes::Issue i;
		i.message(e.what());
		r.issue().push_back(i);	
	}
	catch (...)
	{
		r.validResult(false);
		commonTypes::Issue i;
		i.message("Unknown Error");
		r.issue().push_back(i);
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

	std::ifstream instream(inFile);
	if (!instream.good())
	{
		*logFileStream << "Invalid input file: " << inFile << std::endl;
		return -1;
	}

	std::set<Issue> issues; // issues at fuzztree level
	FuzzTreeTransform tf(instream, issues);
	instream.close();

	backendResults::BackendResults analysisResults;
	try
	{	
		// please keep this here for debugging
// 		std::istreambuf_iterator<char> eos;
// 		std::string s(std::istreambuf_iterator<char>(instream), eos);
// 		*logFileStream << s;

		if (!tf.isValid())
		{ // handle faulttree
			std::ifstream is(inFile); // TODO: somehow avoid opening another stream here
			const std::auto_ptr<faulttree::FaultTree> faultTree = 
				faulttree::faultTree(inFile, xml_schema::Flags::dont_validate);
			is.close();

			std::vector<Issue> treeIssues;
			const unsigned int decompositionNumber = 
				faultTree->topEvent().decompositionNumber().present() ? 
				faultTree->topEvent().decompositionNumber().get() : 
				DEFAULT_DECOMPOSITION_NUMBER;
			const auto modelId = faultTree->id();
			const auto configId = "0"; // TODO find a default id
			backendResults::AnalysisResult r(modelId, configId, util::timeStamp(), true, decompositionNumber);
			r.decompositionNumber(decompositionNumber);
			try
			{
				const auto topEvent = faultTreeToFuzzTree(faultTree->topEvent(), treeIssues);	
				analyze(r, topEvent.get(), logFileStream, decompositionNumber);
			}
			catch (const FatalException& e)
			{
				r.issue().push_back(e.getIssue().serialized());
				r.validResult(false);
			}
			for (const auto& i : treeIssues)
				r.issue().push_back(i.serialized());
			
			analysisResults.result().push_back(r);

			if (!r.validResult())
				faulttree::faultTree(*logFileStream, *(faultTree.get()));
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
				backendResults::AnalysisResult r(modelId, t.first.getId(), util::timeStamp(), true, decompositionNumber);
				try
				{
					analyze(r, &topEvent, logFileStream, decompositionNumber);
				}
				catch (const FatalException& e)
				{
					r.issue().push_back(e.getIssue().serialized());
					r.validResult(false);
				}
				 
				analysisResults.configuration().push_back(serializedConfiguration(t.first));
				analysisResults.result().push_back(r);
			}
		}
	}

	catch (const std::exception& e)// This should not happen.
	{
		*logFileStream << "Exception while trying to analyze " << inFile << e.what() << std::endl;
	}
	catch (...)
	{
		*logFileStream << "Exception while trying to analyze " << inFile << std::endl;
	}

	// Log errors
	for (const Issue& issue : issues)
	{
		analysisResults.issue().push_back(issue.serialized());
		*logFileStream << issue.getMessage() << std::endl;
	}

	std::ofstream output(outFile);
	backendResults::backendResults(output, analysisResults);
	
	logFileStream->close();
	delete logFileStream;

	return 0;
}
