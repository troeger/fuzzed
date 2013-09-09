#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "AnalysisResult.h"
#include "util.h"

#include <fstream>
#include <iostream>

int main()
{
	const std::string testfile = "C:\\dev\\fuzztrees\\backends\\fuzztreeanalysis\\testdata\\EWDC2013.fuzztree"; // "C:\\dev\\fuzztrees\\backends\\simulation\\testdata\\mixed.fuzztree";
	std::ifstream file(testfile);
	if (!file.is_open())
		return -1;
	try
	{
		auto t = fuzztree::fuzzTree(file, xml_schema::Flags::dont_validate);
		file.close();

		auto topEvent = fuzztree::TopEvent(t->topEvent());
		
		const int dn = 10; // TODO where does this come from?

		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, dn);
		const auto result = analysis->compute();

		std::string xmlFile = testfile;
		util::replaceFileExtensionInPlace(xmlFile, ".xml");

		AnalysisResult resultDocument;
		resultDocument.setModelId(t->id());
		resultDocument.setDecompositionNumber(dn);
		resultDocument.addConfiguration(result);
		resultDocument.save(xmlFile);
	}
	catch (const std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

	return 0;
}