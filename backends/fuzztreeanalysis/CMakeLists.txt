project(fuzztreeanalysis)

set(SOURCES
  main.cpp
  AlphaCutAnalysisTask.cpp
  InstanceAnalysisTask.cpp
  AnalysisResult.cpp
)

set(HEADERS
  AlphaCutAnalysisTask.h
  InstanceAnalysisTask.h
  AnalysisResult.h
)

add_executable(ftanalysis_exe ${SOURCES} ${HEADERS})
target_link_libraries(ftanalysis_exe common_model ftconfiguration pugixml)
