set(FT_CONFIG_DIR "${PROJECT_SOURCE_DIR}/fuzztreeconfiguration")
set(FT_INCLUDE_DIR
  "${CMAKE_CURRENT_SOURCE_DIR}/modeltransform"
  "${CMAKE_CURRENT_SOURCE_DIR}/simulation"
  "${CMAKE_CURRENT_SOURCE_DIR}/fuzztreeconfiguration"
  "${CMAKE_CURRENT_SOURCE_DIR}/util")

option(BUILD_SIMULATION_EXECUTABLE ON)
option(USE_TIMENET ON)

set(SIM_COMMON_SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/util/FaultTreeImport.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/util/XMLImport.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/util/Condition.cpp
)

set(SIM_COMMON_HEADERS
  ${CMAKE_CURRENT_SOURCE_DIR}/util/Types.h
  ${CMAKE_CURRENT_SOURCE_DIR}/util/FaultTreeImport.h
  ${CMAKE_CURRENT_SOURCE_DIR}/util/XMLImport.h
  ${CMAKE_CURRENT_SOURCE_DIR}/util/Constants.h
  ${CMAKE_CURRENT_SOURCE_DIR}/util/Condition.h
)

include_directories(${FT_INCLUDE_DIR})


add_subdirectory(modeltransform)
add_subdirectory(simulation)