project(ftmincuts)

set(SOURCES
  main.cpp
  MinCutAnalysisTask.cpp
)

set(HEADERS
  MinCutAnalysisTask.h
  MinCut.h
)

add_executable(ftmincuts ${SOURCES} ${HEADERS})
target_link_libraries(ftmincuts common_model ftconfiguration)