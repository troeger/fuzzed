#pragma once

#include "platform.h"

extern "C"
{
	void /*FT_DLL_API*/ runSimulationOnFile(
		char* filePath,					/* path to fault tree file */
		int numRounds,					/* the max number of simulation rounds. if convergence is specified, the actual number may be lower*/
		double convergenceThreshold,	/* stop after reliability changes no more than this threshold */
		int maxTime						/* maximum duration of simulation in milliseconds */
		) noexcept;
}

