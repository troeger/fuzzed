#include "InstanceAnalysisTask.h"
#include "AlphaCutAnalysisTask.h"
#include "AnalysisResult.h"

#include <string>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/program_options.hpp>
#include <iostream>
#include <fstream>

#include "util.h"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

using std::endl;
using std::cout;
using std::string;

int main(int argc, char** argv)
{
	// const std::string testfile = "C:\\dev\\fuzztrees\\backends\\fuzztreeanalysis\\testdata\\EWDC2013.fuzztree"; // "C:\\dev\\fuzztrees\\backends\\simulation\\testdata\\mixed.fuzztree";
	try
	{
		string outDir, inFile;
		bool generateFaultTree;

		po::options_description options;
		options.add_options()
			("help,h", "produce help message")
			("infile,i",		po::value<string>(&inFile),		"Path to FuzzTree file")
			("outdir,o",		po::value<string>(&outDir),		"Output directory for FuzzTree or faulttree files")
			("faulttree,f",		po::value<bool>(&generateFaultTree));

		po::variables_map optionsMap;
		po::store(po::parse_command_line(argc, argv, options), optionsMap);
		po::notify(optionsMap);

		if (optionsMap.count("help")) 
		{
			cout << options << endl;
			return -1;
		}
		else if (optionsMap.count("infile") == 0 || optionsMap.count("outdir") == 0)
		{
			cout << "Please specify input file and output directory." << endl;
			cout << options << endl;
			return -1;
		}

		const auto dirPath = fs::path(outDir.c_str());
		const auto inFilePath = fs::path(inFile.c_str());
		if (!fs::is_directory(dirPath))
		{
			cout << "Not a valid directory name: " << dirPath << endl;
			return -1;
		}
		else if (!(status(dirPath).permissions() & fs::owner_write))
		{
			cout << "Cannot write to folder: " << dirPath << endl;
			return -1;
		}
		else if (!fs::is_regular_file(inFilePath))
		{
			cout << "Not a valid file name: " << inFile << endl;
			return -1;
		}

		std::ifstream file(inFile);
		auto t = fuzztree::fuzzTree(file, xml_schema::Flags::dont_validate);
		file.close();

		auto topEvent = fuzztree::TopEvent(t->topEvent());
		
		const int dn = 10; // TODO where does this come from?

		InstanceAnalysisTask* analysis = new InstanceAnalysisTask(&topEvent, dn);
		const auto result = analysis->compute();

		std::string xmlFile = util::fileNameFromPath(inFile);
		util::replaceFileExtensionInPlace(xmlFile, ".xml");

		AnalysisResult resultDocument;
		resultDocument.setModelId(t->id());
		resultDocument.setDecompositionNumber(dn);
		resultDocument.addConfiguration(result);
		resultDocument.save(outDir + "/" + xmlFile);
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