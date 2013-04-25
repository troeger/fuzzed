project(fttransform CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   main.cpp
   SimulationProxy.cpp

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

add_executable(ftsimulation ${SOURCES} ${HEADERS})

if (WIN32)
	target_link_libraries(ftsimulation optimized ${FT_LIB_DIR}/Release/ftmodeltransform.lib)
	target_link_libraries(ftsimulation debug ${FT_LIB_DIR}/Debug/ftmodeltransform.lib)
	target_link_libraries(ftsimulation optimized ${FT_LIB_DIR}/Release/ftcommon.lib)
	target_link_libraries(ftsimulation debug ${FT_LIB_DIR}/Debug/ftcommon.lib)
endif (WIN32)

if (UNIX)
	target_link_libraries(ftsimulation optimized ${FT_LIB_DIR}/libftmodeltransform.a)
	target_link_libraries(ftsimulation debug ${FT_LIB_DIR}/libftmodeltransform.a)
	target_link_libraries(ftsimulation optimized ${FT_LIB_DIR}/libftcommon.a)
	target_link_libraries(ftsimulation debug ${FT_LIB_DIR}/libftcommon.a)
	message("Linking against static libs")
endif (UNIX)

message("Building Simulation Executable")

option(profileOMP "Profile OpenMP" ON)
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
endif(WIN32)
