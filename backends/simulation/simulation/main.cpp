#include "SimulationProxy.h"
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
	try
	{
		SimulationProxy proxy(argc, argv);
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
