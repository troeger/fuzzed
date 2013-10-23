#pragma once

#include <configurations.h>
#include "FuzzTreeConfiguration.h"

configurations::Configuration serializedConfiguration(const FuzzTreeConfiguration &c);

#define DEFAULT_DECOMPOSITION_NUMBER 10
#define DEFAULT_MISSION_TIME 17520