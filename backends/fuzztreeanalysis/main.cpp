#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "FuzzTreeTransform.h"

#include <string>
#include <iostream>
#include <fstream>

#include "CommandLineParser.h"
#include "util.h"
#include "xmlutil.h"
#include "analysisResult.h"

int main(int argc, char** argv)
{
	CommandLineParser parser;
	parser.parseCommandline(argc, argv);
	const auto inFile = parser.getInputFilePath().generic_string();
	const auto outFile = parser.getOutputFilePath().generic_string();

	try
	{
		std::ifstream instream(inFile);
		if (!instream.good())
		{
			std::cerr << "Invalid input file: " << inFile << std::endl;
			return -1;
		}
		auto tree = fuzztree::fuzzTree(instream, xml_schema::Flags::dont_validate);

		unsigned int decompositionNumber = DEFAULT_DECOMPOSITION_NUMBER;
		if (tree->topEvent().decompositionNumber().present())
			decompositionNumber = tree->topEvent().decompositionNumber().get();

		const auto modelId = tree->id();

		analysisResults::AnalysisResults analysisResults;

		FuzzTreeTransform tf(tree);
		if (!tf.isValid())
		{
			std::cerr << "Could not compute configurations." << std::endl;
			return -1;
		}
		
		for (const auto& t : tf.transform())
		{
			auto topEvent = fuzztree::TopEvent(t.second.topEvent());
			InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, decompositionNumber);
			const auto result = analysis->compute();

			analysisResults::Result r(modelId, util::timeStamp(), true, decompositionNumber);
			r.configuration(serializedConfiguration(t.first));
			r.probability(serialize(result));
			analysisResults.result().push_back(r);
		}
		std::ofstream output(outFile);
		analysisResults::analysisResults(output, analysisResults);
	}
	catch (const std::exception& e)
	{
		std::cerr << "Exception while trying to analyze" << inFile << e.what() << std::endl;
		return -1;
	}
	catch (...)
	{
		std::cerr << "Exception while trying to analyze" << inFile << std::endl;
		return -1;
	}

	return 0;
}
