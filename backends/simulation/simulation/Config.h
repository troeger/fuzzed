#pragma once

#define WINDOWS defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)

const char* const RAND_FILE = "C:/dev/masterarbeit/simulation/implementation/randomnumbers/rand_.txt";

// TimeNET parameters
#define DEFAULT_CONFIDENCE 90
#define DEFAULT_EPSILON 10

// Simulation parameters
#define DEFAULT_SIMULATION_TIME 10
#define DEFAULT_SIMULATION_STEPS 1000
#define DEFAULT_SIMULATION_ROUNDS 2000

#define DEFAULT_SIMULATION_OUTPUT_PREFIX "../simulationoutput/"

#define PAR_THRESH 10 // if less rounds are executed, don't even parallelize


/************************************************************************/
/* The following macros are for profiling only.                         */
/************************************************************************/

// #define NUM_MONTE_CARLO_ROUNDS 1000			// run many Monte Carlo simulations, e.g. for estimating the variance in the results
// #define RELIABILITY_DISTRIBUTION				// compute the entire reliability distribution up to mission time, for statistical tests
// #define MEASURE_SPEEDUP true					// do one simulation run for all possible numbers of threads

// #define OMP_PARALLELIZATION			// use OpenMP to parallelize. alternative: manual (static) work splitting over a number of C++11 threads 
