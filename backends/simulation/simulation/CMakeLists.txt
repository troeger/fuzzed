project(ftsimulation)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCES}
   ${SIM_COMMON_SOURCES}

   main.cpp
   SimulationProxy.cpp

   implementation/PetriNetSimulation.cpp
   implementation/Random.cpp

   petrinet/Place.cpp
   petrinet/Transition.cpp
   petrinet/TimedTransition.cpp
   petrinet/ImmediateTransition.cpp
   petrinet/PNMLImport.cpp
   petrinet/PetriNet.cpp
)

set(HEADERS
   ${HEADERS}
   ${SIM_COMMON_HEADERS}

   SimulationProxy.h
   ResultStruct.h
   Config.h
   
   implementation/PetriNetSimulation.h
   implementation/Simulation.h
   implementation/Random.h

   petrinet/Place.h
   petrinet/Transition.h
   petrinet/TimedTransition.h
   petrinet/ImmediateTransition.h
   petrinet/PNMLImport.h
   petrinet/PetriNet.h
)

if (USE_OMP)
	find_package(OpenMP REQUIRED)
	if (OPENMP_FOUND)
		message("OPENMP FOUND")
		set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
		set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
	endif()
endif()

add_executable(ftsimulation ${SOURCES} ${HEADERS})
target_link_libraries(ftsimulation pugixml common_model ftconfiguration ftmodeltransform)
