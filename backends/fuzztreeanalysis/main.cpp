#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "AnalysisResultDocument.h"
#include "FuzzTreeTransform.h"

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

		std::ifstream stream(inFile);
		assert(stream.good());
		auto tree = fuzztree::fuzzTree(stream, xml_schema::Flags::dont_validate);
		
		const int decompositionNumber = tree->topEvent().decompositionNumber();

		AnalysisResultDocument resultDocument;
		resultDocument.setModelId(tree->id());
		resultDocument.setDecompositionNumber(decompositionNumber);

		FuzzTreeTransform tf(tree);
		for (const auto& t : tf.transform())
		{
			auto topEvent = fuzztree::TopEvent(t.second.topEvent());
			InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, decompositionNumber);
			
			const auto result = analysis->compute();
			resultDocument.addConfigurationResult(t.first, result);
		}
		resultDocument.setValid(true);
		resultDocument.setTimeStamp(util::timeStamp());
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