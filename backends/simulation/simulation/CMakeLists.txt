project(ftsimulation CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCES}
   ${SIM_COMMON_SOURCES}

   main.cpp
   StructureFormulaClient.cpp
   SimulationClient.cpp
   SimulationExtern.cpp
   SimulationProxy.cpp
   ResultDocument.cpp

   implementation/PetriNetSimulation.cpp
   implementation/TimeNETSimulation.cpp
   implementation/Random.cpp

   petrinet/Place.cpp
   petrinet/Transition.cpp
   petrinet/TimedTransition.cpp
   petrinet/ImmediateTransition.cpp
   petrinet/PNMLImport.cpp
   petrinet/PetriNet.cpp
   petrinet/SequentialConstraint.cpp
)

set(HEADERS
   ${HEADERS}
   ${SIM_COMMON_HEADERS}

   StructureFormulaClient.h
   SimulationClient.h
   SimulationExtern.h
   SimulationProxy.h
   ResultDocument.h
   ResultStruct.h
   Config.h

   beanstalkdconfig.h
   
   implementation/PetriNetSimulation.h
   implementation/TimeNETSimulation.h
   implementation/Simulation.h
   implementation/Random.h

   petrinet/Place.h
   petrinet/Transition.h
   petrinet/TimedTransition.h
   petrinet/ImmediateTransition.h
   petrinet/PNMLImport.h
   petrinet/PetriNet.h
   petrinet/SequentialConstraint.h
   petrinet/PetriNetConstraint.h
)

if (USE_TIMENET)
	find_package(TimeNET REQUIRED)
endif (USE_TIMENET)

find_package(OpenMP REQUIRED)
if (OPENMP_FOUND)
	message("OPENMP FOUND")
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
	set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif ()

if (BUILD_SIMULATION_EXECUTABLE)
   add_executable(ftsimulation ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation
      ${COMMON_LINKED_LIBS}
	  ftmodeltransform
      ftconfiguration
   )
   message("Building simulation executable")
else (BUILD_SIMULATION_EXECUTABLE) # shared library
   add_library(ftsimulation SHARED ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation
	  ${COMMON_LINKED_LIBS}
      ftmodeltransform
	  ftconfiguration
   )
   add_definitions(-DSIMULATION_DLL)
   message("Building shared simulation library")
endif (BUILD_SIMULATION_EXECUTABLE)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${PUGIXML_INCLUDE_DIR})

if (BUILD_TESTS)
   add_library(ftsimulation_static STATIC ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation_static
      ftmodeltransform
	  ${FT_CONFIG_LIB}
   )
   set_target_properties(ftsimulation_static PROPERTIES COMPILE_DEFINITIONS "SIMULATION_STATIC")
endif(BUILD_TESTS)
