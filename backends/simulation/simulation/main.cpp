#include "SimulationProxy.h"
#include <iostream>
#include "GraphParser.h"
#include "CommandLineParser.h"

using namespace std;

int main(int argc, char** argv)
{
	try
	{
		//SimulationProxy proxy(argc, argv);

		CommandLineParser parser;
		parser.parseCommandline(argc, argv);
		const auto inFile	= parser.getInputFilePath().generic_string();
		const auto outFile	= parser.getOutputFilePath().generic_string();
		const auto logFile	= parser.getLogFilePath().generic_string();

		std::ofstream logStream(logFile);
		const auto res = GraphParser::fromGraphML(inFile, logStream.good() ? &logStream : nullptr);
	}
	catch (exception& e)
	{
		cout << "Exception during Simulation: " << e.what() << endl;
		return -1;
	}
	catch (...)
	{
		cout << "Unknown error in SimulationProxy" << endl;
		return -1;
	}
	return 0;
}
