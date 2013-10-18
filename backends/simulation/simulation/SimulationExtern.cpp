#include "SimulationExtern.h"
#include "SimulationProxy.h"
#include "FuzzTreeTransform.h"
#include "FaultTreeConversion.h"
#include "FaultTreeIncludes.h"
#include "util.h"

#include <iostream>

using namespace std;

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
