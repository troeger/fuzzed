project(fuzztreeconfiguration)

set(SOURCES
  FuzzTreeConfiguration.cpp
  main.cpp
)

set(HEADERS
  FuzzTreeConfiguration.h
  platform.h
)

include_directories()

# Compile as library for usage from analysis executable
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS})
target_link_libraries(ftconfiguration common_model)

# compile as executable for explicit configuration determination
add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS})
target_link_libraries(ftconfiguration_exe common_model)
