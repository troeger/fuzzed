project(fuzztreeanalysis)

set(SOURCES
  main.cpp
  AlphaCutAnalysisTask.cpp
  InstanceAnalysisTask.cpp
  Probability.cpp
  DecomposedFuzzyInterval.cpp
)

set(HEADERS
  AlphaCutAnalysisTask.h
  InstanceAnalysisTask.h
  Interval.h
  DecomposedFuzzyInterval.h
  Probability.h
)

add_executable(ftanalysis_exe ${SOURCES} ${HEADERS})
target_link_libraries(ftanalysis_exe common_model ftconfiguration)
