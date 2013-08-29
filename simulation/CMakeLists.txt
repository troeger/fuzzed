set(FT_CONFIG_DIR "${PROJECT_SOURCE_DIR}/fuzztreeconfiguration")
set(FT_INCLUDE_DIR
  "${CMAKE_CURRENT_SOURCE_DIR}/modeltransform"
  "${CMAKE_CURRENT_SOURCE_DIR}/simulation" 
  "${CMAKE_CURRENT_SOURCE_DIR}/common"
  "${CMAKE_CURRENT_SOURCE_DIR}/fuzztreeconfiguration")

option(BUILD_SIMULATION_EXECUTABLE ON)
option(USE_TIMENET ON)

add_subdirectory(common)
add_subdirectory(modeltransform)
add_subdirectory(simulation)