project(ftmincuts)

set(SOURCES
  main.cpp
  MincutAnalysisTask.cpp
)

set(HEADERS
  MincutAnalysisTask.h
)

add_executable(ftmincuts ${SOURCES} ${HEADERS})
target_link_libraries(ftmincuts common_model ftconfiguration)
