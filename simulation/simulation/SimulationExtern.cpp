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
	int missionTime, 
	int numRounds,
	double convergenceThreshold,
	int maxTime) noexcept
{	
	try
	{
		SimulationProxy p = SimulationProxy(missionTime, numRounds, convergenceThreshold, maxTime);
		
		FuzzTreeTransform ftTransform(fuzztreeXML);
		int i = 0;
		for (const auto& ft : ftTransform.transform())
		{
			p.simulateFaultTree(fromGeneratedFaultTree(ft.topEvent()), "foo" + util::toString(++i) + ".TN", TIMENET);
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
	int missionTime, 
	int numRounds,
	double convergenceThreshold,
	int maxTime) noexcept
{	
	try
	{
		SimulationProxy p = SimulationProxy(missionTime, numRounds, convergenceThreshold, maxTime);
		p.simulateFile(filePath, DEFAULT, false); // TODO make configurable

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
