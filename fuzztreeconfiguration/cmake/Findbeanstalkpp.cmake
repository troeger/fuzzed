find_path(BEANSTALKPP_INCLUDE beanstalkpp.h
    ${PROJECT_SOURCE_DIR}/thirdParty/beanstalkpp
)

find_library(BEANSTALKPP_LIB beanstalkpp PATHS ${PROJECT_SOURCE_DIR}/thirdParty/beanstalkpp)

if (NOT BEANSTALKPP_LIB OR NOT BEANSTALKPP_INCLUDE)
	message(FATAL_ERROR "Could not find beanstalkpp.")
endif()
