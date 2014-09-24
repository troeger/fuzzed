#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"

#include <string>
#include <iostream>
#include <fstream>

#include "FatalException.h"
#include "CommandLineParser.h"
#include "util.h"

#include "Model.h"
#include "AnalysisResult.h"
#include "resultxml.h"
#include "FuzzTreeToFaultTree.h"

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
	// please keep this here for debugging
	std::istreambuf_iterator<char> eos;
	std::ifstream inputFileStream(inFile);
	std::string s(std::istreambuf_iterator<char>(inputFileStream), eos);
	*logFileStream << "Analysis input file: " << s << std::endl;
	inputFileStream.close();

	// Analyze
	std::vector<AnalysisResult> results;
	Model m(inFile);
	ResultsXML xml;

	const unsigned int decompositionNumber = m.getDecompositionNumber();
	const unsigned int missionTime = m.getMissionTime();
	const std::string modelId = m.getId();

	if (m.getType() == modeltype::FUZZTREE)
	{
		FuzzTreeToFaultTree transform(&m);
		const auto configs = transform.generateConfigurations();
		for (const FuzzTreeConfiguration& inst : configs)
		{
			Model faultTree = transform.faultTreeFromConfiguration(inst);
			InstanceAnalysisTask analysis(faultTree.getTopEvent(), decompositionNumber, missionTime, *logFileStream);
			DecomposedFuzzyInterval result = analysis.compute();
			results.emplace_back(modelId, inst.getId(), util::timeStamp(), result);
		}

		xml.generate(configs, results, std::ofstream(outFile));
	}
	else
	{
		InstanceAnalysisTask analysis(m.getTopEvent(), decompositionNumber, missionTime, *logFileStream);
		DecomposedFuzzyInterval result = analysis.compute();
		results.emplace_back(modelId, "", util::timeStamp(), result);

		xml.generate(results, std::ofstream(outFile));
	}
	
	// TODO: Report all issues

	logFileStream->close();
	delete logFileStream;

	return 0;
}
