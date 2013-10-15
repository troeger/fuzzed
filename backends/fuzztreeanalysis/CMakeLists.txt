project(fuzztreeanalysis CXX)

set(SOURCES
  main.cpp
  AlphaCutAnalysisTask.cpp
  InstanceAnalysisTask.cpp
  Probability.cpp
  DecomposedFuzzyInterval.cpp
  AnalysisResultDocument.cpp
)

set(HEADERS
  AlphaCutAnalysisTask.h
  InstanceAnalysisTask.h
  Interval.h
  DecomposedFuzzyInterval.h
  Probability.h
  AnalysisResultDocument.h
)

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
endif (BUILD_TESTS)
