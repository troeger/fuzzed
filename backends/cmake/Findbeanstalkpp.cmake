find_path(BEANSTALKPP_INCLUDE beanstalkpp.h
    ${PROJECT_SOURCE_DIR}/thirdParty/beanstalkpp)

find_library(BEANSTALKPP_LIB_DEBUG
  NAMES beanstalkppd beanstalkpp
  PATHS
  ${PROJECT_SOURCE_DIR}/thirdParty/beanstalkpp
  ${FT_LIB_DIR})

find_library(BEANSTALKPP_LIB_RELEASE
  NAMES beanstalkpp
  PATHS
  ${PROJECT_SOURCE_DIR}/thirdParty/beanstalkpp
  ${FT_LIB_DIR})

set(BEANSTALKPP_LIB
  debug ${BEANSTALKPP_LIB_DEBUG}
  optimized ${BEANSTALKPP_LIB_RELEASE})

if (NOT BEANSTALKPP_LIB OR NOT BEANSTALKPP_INCLUDE)
	message(FATAL_ERROR "Could not find beanstalkpp.")
endif()