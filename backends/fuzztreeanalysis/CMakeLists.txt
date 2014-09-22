project(fuzztreeanalysis)

set(SOURCES
  main.cpp
  AlphaCutAnalysisTask.cpp
  InstanceAnalysisTask.cpp
)

set(HEADERS
  AlphaCutAnalysisTask.h
  InstanceAnalysisTask.h
)

add_executable(ftanalysis_exe ${SOURCES} ${HEADERS})
target_link_libraries(ftanalysis_exe common_model ftconfiguration)
