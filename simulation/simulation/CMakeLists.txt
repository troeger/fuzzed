project(ftsimulation CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   main.cpp
   SimulationProxy.cpp
   ResultDocument.cpp

   implementation/PetriNetSimulation.cpp
   implementation/TimeNETSimulation.cpp
   implementation/Random.cpp

   petrinet/Place.cpp
   petrinet/Transition.cpp
   petrinet/TimedTransition.cpp
   petrinet/ImmediateTransition.cpp
   petrinet/TransitionCondition.cpp
   petrinet/PNMLImport.cpp
   petrinet/PetriNet.cpp
)
set(HEADERS
   ${HEADERS}
   SimulationProxy.h
   ResultDocument.h
   ResultStruct.h
   Config.h
   
   implementation/PetriNetSimulation.h
   implementation/TimeNETSimulation.h
   implementation/Simulation.h
   implementation/Random.h

   petrinet/Place.h
   petrinet/Transition.h
   petrinet/TimedTransition.h
   petrinet/ImmediateTransition.h
   petrinet/TransitionCondition.h
   petrinet/PNMLImport.h
   petrinet/PetriNet.h
)

if (BUILD_SIMULATION_EXECUTABLE)
   add_executable(ftsimulation ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation
      ftmodeltransform
      ftconfiguration
      ftcommon
   )
   message("Building simulation executable")
else (BUILD_SIMULATION_EXECUTABLE) # shared library
   add_library(ftsimulation SHARED ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation 
      ftmodeltransform      
ftconfiguration
      ftcommon
   )
   add_definitions(-DSIMULATION_DLL)
   message("Building shared simulation library")
endif (BUILD_SIMULATION_EXECUTABLE)

option(profileOMP "Profile OpenMP" OFF)
find_package(OpenMP)
if (OPENMP_FOUND)
	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
	if (${profileOMP} AND UNIX)
		find_package(ompP REQUIRED)
		# compile with ompP compiler
		# somehow this works only on the command line
		#set(CMAKE_CXX_COMPILER "${OMPP_CXX} ${CMAKE_CXX_COMPILER}")
		#set(CMAKE_C_COMPILER "${OMPP_CC} ${CMAKE_C_COMPILER}")
		message("Profiling OpenMP")
		include_directories(${OMPP_INCLUDE_DIR})
		target_link_libraries(ftsimulation ${OMPP_LIB_DIR}/libompp.a)
	endif()
endif()

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

target_link_libraries(ftsimulation ${Boost_LIBRARIES})
if (WIN32)
   target_link_libraries(ftsimulation optimized ${PUGIXML_LIB_RELEASE})
   target_link_libraries(ftsimulation debug ${PUGIXML_LIB_DEBUG})
endif (WIN32)

if (BUILD_TESTS)
   add_library(ftsimulation_static STATIC ${SOURCES} ${HEADERS})
   target_link_libraries(ftsimulation_static
      ftmodeltransform
      ftconfiguration
      ftcommon
   )
endif (BUILD_TESTS)
