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
