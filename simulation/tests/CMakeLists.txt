project(Tests)

set(SOURCES
	${SOURCE}
	main.cpp
	
	SerializationTests.cpp
	FaultTreeTests.cpp
	ImportTests.cpp
)

if(MSVC) # VS2012 doesn't support correctly the tuples yet
	add_definitions( /D _VARIADIC_MAX=10 )
endif()

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ../dll)

add_executable(Tests ${SOURCES} ${HEADERS})

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})
include_directories(${GTEST_INCLUDE_DIR})
target_link_libraries(Tests ${GTEST_LIB})

include_directories(${PUGIXML_INCLUDE_DIR})
target_link_libraries(Tests optimized ${PUGIXML_LIB_RELEASE})
target_link_libraries(Tests debug ${PUGIXML_LIB_DEBUG})

target_link_libraries(Tests optimized ${FT_LIB_DIR}/Release/ftmodeltransform.lib)
target_link_libraries(Tests debug ${FT_LIB_DIR}/Debug/ftmodeltransform.lib)
target_link_libraries(Tests optimized ${FT_LIB_DIR}/Release/ftcommon.lib)
target_link_libraries(Tests debug ${FT_LIB_DIR}/Debug/ftcommon.lib)