#include "FaultTreeIncludes.h"
#include "import/FaultTreeImport.h"
#include "serialization/PNMLDocument.h"
#include "util.h"

#if IS_WINDOWS 
	#pragma warning(push, 3) 
#endif
#include <boost/range/irange.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/foreach.hpp>
#include <map>
#include <gtest/gtest.h>
#if IS_WINDOWS 
	#pragma warning(pop) 
#endif


const string sample = "C:/dev/masterarbeit/testdata/sample_fuzztree.fuzztree";
const string inputfolder = "C:/dev/masterarbeit/testdata/";
const string folder = "C:/dev/masterarbeit/tests/output/";

TEST(ImportFile, SimpleFile)
{
	FaultTreeNode* tree = FaultTreeImport::loadFaultTree(sample);
	tree->print(std::cout);
	EXPECT_TRUE(tree->getNumChildren() > 0);
	
	boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
	EXPECT_NO_FATAL_FAILURE(tree->serialize(doc));
	doc->save(folder+"sample_fuzztree.pnml");
}

TEST(ImportFile, TestFiles)
{
	boost::filesystem::directory_iterator it(boost::filesystem::path(inputfolder.c_str())), eod;
	BOOST_FOREACH(boost::filesystem::path const &p, std::make_pair(it, eod))   
	{ 
		if (is_regular_file(p) && p.extension() == ".fuzztree")
		{
			FaultTreeNode* tree = FaultTreeImport::loadFaultTree(p.generic_string());
			tree->print(std::cout);
			EXPECT_TRUE(tree->getNumChildren() > 0);

			boost::shared_ptr<PNMLDocument> doc(new PNMLDocument());
			if (!tree->isValid())
			{
				EXPECT_FALSE(true);
				continue;
			}
			EXPECT_NO_FATAL_FAILURE(tree->serialize(doc));

			string fileName = p.generic_string();
			util::replaceStringInPlace(fileName, ".fuzztree", ".pnml");

			doc->save(folder + fileName);
		} 
	}
	
	
}