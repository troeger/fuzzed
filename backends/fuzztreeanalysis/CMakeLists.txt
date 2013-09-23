project(fuzztreeanalysis CXX)

set(SOURCES
  main.cpp
  AlphaCutAnalysisTask.cpp
  InstanceAnalysisTask.cpp
  Probability.cpp
  DecomposedFuzzyInterval.cpp
  AnalysisResult.cpp
)

set(HEADERS
  AlphaCutAnalysisTask.h
  InstanceAnalysisTask.h
  Interval.h
  DecomposedFuzzyInterval.h
  Probability.h
  AnalysisResult.h
)

include_directories(${BEANSTALKPP_INCLUDE})
include_directories(${PUGIXML_INCLUDE_DIR})

add_executable(ftanalysis ${SOURCES} ${HEADERS})
  target_link_libraries(ftanalysis
    ${FT_CONFIG_LIB}
    ${COMMON_LINKED_LIBS})
  message("Building analysis executable")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

if (BUILD_TESTS)
  add_library(ftanalysis_static STATIC ${SOURCES} ${HEADERS})
  target_link_libraries(ftanalysis_static
    ${FT_CONFIG_LIB}
    ${XERCESC_LIBRARIES})
  set_target_properties(ftanalysis_static PROPERTIES COMPILE_DEFINITIONS "ANALYSIS_STATIC")
endif (BUILD_TESTS)
