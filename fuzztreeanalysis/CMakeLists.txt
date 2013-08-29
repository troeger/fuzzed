project(fuzztreeanalysis CXX)

set(SOURCES
   main.cpp
   AlphaCutAnalysisTask.cpp
   InstanceAnalysisTask.cpp
   Probability.cpp
)

set(HEADERS
   AlphaCutAnalysisTask.h
   InstanceAnalysisTask.h
   Interval.h
   DecomposedFuzzyInterval.h
   Probability.h
)

find_package(beanstalkpp REQUIRED)
message(STATUS "Found Beanstalk Client lib: ${BEANSTALKPP_LIB}")
include_directories(${BEANSTALKPP_INCLUDE})

message("${FT_CONFIG_LIB}")

option(BUILD_ANAlYSIS_EXECUTABLE ON)
if (BUILD_ANAlYSIS_EXECUTABLE)
   add_executable(ftanalysis ${SOURCES} ${HEADERS})
   target_link_libraries(ftanalysis
    ${FT_CONFIG_LIB}
    ${Boost_LIBRARIES}
   )
   message("Building analysis executable")
else (BUILD_ANAlYSIS_EXECUTABLE) # shared library
   add_library(ftanalysis SHARED ${SOURCES} ${HEADERS})
   target_link_libraries(ftanalysis 
    ${FT_CONFIG_LIB}
    ${Boost_LIBRARIES}
   )
endif (BUILD_ANAlYSIS_EXECUTABLE)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

target_link_libraries(ftanalysis ${Boost_LIBRARIES})
if (WIN32)
   target_link_libraries(ftanalysis optimized ${PUGIXML_LIB_RELEASE})
   target_link_libraries(ftanalysis debug ${PUGIXML_LIB_DEBUG})
endif (WIN32)

if (BUILD_TESTS)
   add_library(ftanalysis_static STATIC ${SOURCES} ${HEADERS})
   target_link_libraries(ftanalysis_static
    ${FT_CONFIG_LIB}
   )
   set_target_properties(ftanalysis_static PROPERTIES COMPILE_DEFINITIONS "ANALYSIS_STATIC")
endif (BUILD_TESTS)
