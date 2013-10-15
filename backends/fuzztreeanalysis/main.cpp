#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "AnalysisResultDocument.h"

#include <string>
#include <iostream>
#include <fstream>

#include "CommandLineParser.h"
#include "util.h"


using std::endl;
using std::cerr;
using std::string;

int main(int argc, char** argv)
{
	try
	{
		CommandLineParser parser;
		parser.parseCommandline(argc, argv);
		const auto inFile = parser.getInputFilePath().generic_string();
		const auto outFile = parser.getOutputFilePath().generic_string();

		std::ifstream file(inFile);
		auto t = fuzztree::fuzzTree(file, xml_schema::Flags::dont_validate);
		file.close();

		auto topEvent = fuzztree::TopEvent(t->topEvent());
		
		const int decompositionNumber = 10; // TODO where does this come from?

		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, decompositionNumber);
		const auto result = analysis->compute();

		AnalysisResultDocument resultDocument;
		resultDocument.setModelId(t->id());
		resultDocument.setDecompositionNumber(decompositionNumber);
		resultDocument.addConfiguration(result);
		resultDocument.save(outFile);
	}
	catch (const std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}
	catch (...)
	{
		cout << "Unknown error in Configuration" << endl;
		return -1;
	}

	return 0;
}