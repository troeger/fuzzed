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
		std::ifstream stream(inFile);
		assert(stream.good());
		auto tree = fuzztree::fuzzTree(stream, xml_schema::Flags::dont_validate);

		const int decompositionNumber = tree->topEvent().decompositionNumber();
		const auto modelId = tree->id();

		analysisResults::AnalysisResults analysisResults;

		FuzzTreeTransform tf(tree);
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