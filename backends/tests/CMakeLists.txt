project(Tests CXX)

set(SOURCES
	${SOURCES}
	main.cpp
	
	SerializationTests.cpp
	FaultTreeTests.cpp
	SimulationTests.cpp
	AdvancedSimulationTests.cpp
	TestUtil.h
	TestUtil.cpp
)

if(MSVC) # VS2012 doesn't support correctly the tuples yet
	add_definitions( /D _VARIADIC_MAX=10 )
endif()

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ../dll)

add_executable(Tests ${SOURCES} ${HEADERS})

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${GTEST_INCLUDE_DIR})
target_link_libraries(Tests ${GTEST_LIB})

include_directories(${PUGIXML_INCLUDE_DIR})
include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/../simulation
	${CMAKE_CURRENT_SOURCE_DIR}/../simulation/modeltransform
	${CMAKE_CURRENT_SOURCE_DIR}/../simulation/simulation
	${CMAKE_CURRENT_SOURCE_DIR}/../simulation/util
)

target_link_libraries(Tests optimized ${PUGIXML_LIB_RELEASE})
target_link_libraries(Tests debug ${PUGIXML_LIB_DEBUG})

target_link_libraries(Tests
	ftsimulation_static
	ftconfiguration
	${XERCESC_LIBRARIES}
	ftmodeltransform)