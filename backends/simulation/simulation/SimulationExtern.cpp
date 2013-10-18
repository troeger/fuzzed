#include "SimulationExtern.h"
#include "SimulationProxy.h"
#include "FuzzTreeTransform.h"
#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"
#include "util.h"

#include <iostream>

using namespace std;

void runSimulation(
	char* fuzztreeXML, 
	int numRounds,
	double convergenceThreshold,
	int maxTime) noexcept
{	
	try
	{
		SimulationProxy p = SimulationProxy(numRounds, convergenceThreshold, maxTime);
		
		FuzzTreeTransform ftTransform(fuzztreeXML);
		int i = 0;
		for (const auto& ft : ftTransform.transform())
		{
			p.simulateFaultTree(
				fromGeneratedFuzzTree(ft.second.topEvent()), "foo" + util::toString(++i) + ".TN", TIMENET);
		}

	}
	catch (const exception& e)
	{
		cout << "Unhandled Exception during Simulation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Exception during Simulation" << endl;
	}
}


void runSimulationOnFile(
	char* filePath,
	int numRounds,
	double convergenceThreshold,
	int maxTime) noexcept
{	
	try
	{
		SimulationProxy p = SimulationProxy(numRounds, convergenceThreshold, maxTime);
		p.simulateFile(filePath, DEFAULT);

	}
	catch (const exception& e)
	{
		cout << "Unhandled Exception during Simulation: " << e.what() << endl;
	}
	catch (...)
	{
		cout << "Unknown Exception during Simulation" << endl;
	}
}
