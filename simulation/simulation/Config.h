#pragma once

#define WINDOWS defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)

const char* const RAND_FILE = "C:/dev/masterarbeit/simulation/implementation/randomnumbers/rand_.txt";

// TimeNET parameters
#define DEFAULT_CONFIDENCE 95
#define DEFAULT_EPSILON 0.2f

// Simulation parameters
#define DEFAULT_SIMULATION_TIME 100
#define DEFAULT_SIMULATION_STEPS 1000
#define DEFAULT_SIMULATION_ROUNDS 10000

#define DEFAULT_SIMULATION_OUTPUT_PREFIX "../simulationoutput/"

#define PAR_THRESH 10 // if less rounds are executed, don't even parallelize
