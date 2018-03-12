#pragma once

// This defines the default server to use for the client binaries bundled with the library

#ifndef BEANSTALK_SERVER
#define BEANSTALK_SERVER "127.0.0.1"
#endif

#ifndef BEANSTALK_PORT
#define BEANSTALK_PORT 11300
#endif


#define BEANSTALK_SIM_QUEUE "simulation"
#define BEANSTALK_SIM_RESULT_QUEUE "simulationResults"

#define BEANSTALK_CONFIG_QUEUE "configuration"
#define BEANSTALK_CONFIG_RESULT_QUEUE "configurationResults"