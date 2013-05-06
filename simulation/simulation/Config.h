#pragma once

#define WINDOWS defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)

const char* const RAND_FILE = "C:/dev/masterarbeit/simulation/implementation/randomnumbers/rand_.txt";

#if WINDOWS
#define DEFAULT_FILE_PATH				"C:\\dev\\masterarbeit\\testdata\\blocksim_compare\\single_spare_gate.fuzztree" // "C:\\dev\\masterarbeit\\tests\\output\\"
#else
#define DEFAULT_FILE_PATH				"../tests/output"
#endif

#define DEFAULT_INTEGRATION_PROPS_PATH	"C:/Users/Lena/Documents/Masterarbeit/timeNET/dist/TimeNET/etc/gpsc_conf/integration.props"
#define DEFAULT_LOG_PROPS_PATH			"C:/Users/Lena/Documents/Masterarbeit/timeNET/dist/TimeNET/etc/gpsc_conf/log4j.props"
#define DEFAULT_TIMENET_PATH			"C:/Users/Lena/Documents/Masterarbeit/timeNET/dist/TimeNET/TimeNET.jar"
#define DEFAULT_SIMULATION_TIME 100
#define DEFAULT_SIMULATION_STEPS 1000
#define DEFAULT_SIMULATION_ROUNDS 10000

#define DEFAULT_SIMULATION_OUTPUT_PREFIX "../simulationoutput/"


/************************************************************************/
/* Performance stuff                                                    */
/************************************************************************/
#define PAR_THRESH 10 // if less rounds are executed, don't even parallelize
#define SCHEDULE static //dynamic