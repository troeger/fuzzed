#include "SimulationProxy.h"
#include <iostream>

using namespace std;

#define DEBUG true
#define DETECT_MEM_LEAKS true

#ifdef DETECT_MEM_LEAKS
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
#endif

int main(int argc, char** argv)
{
	try
	{
		SimulationProxy proxy(argc, argv);
	}
	catch (exception& e)
	{
		cout << e.what() << endl;
		return -1;
	}
	catch (...)
	{
		cout << "Unknown error in SimulationProxy" << endl;
		return -1;
	}

#ifdef DETECT_MEM_LEAKS
	_CrtDumpMemoryLeaks();
#endif
	return 0;
}
