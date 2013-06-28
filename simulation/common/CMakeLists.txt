project(common)

set(LIBNAME ftcommon)
set(FTCOMMON_LIB ${LIBNAME} PARENT_SCOPE)

set(SOURCES
	${SOURCES}
	
	util.cpp
	XMLImport.cpp
	FaultTreeImport.cpp
)

set(HEADERS
	${HEADERS}

	platform.h
	util.h
	XMLImport.h
	FaultTreeImport.h
	Types.h
	Constants.h
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

if (WIN32)
	add_library(${LIBNAME} STATIC ${SOURCES} ${HEADERS})
	target_link_libraries(ftcommon optimized ${PUGIXML_LIB_RELEASE})
	target_link_libraries(ftcommon debug ${PUGIXML_LIB_DEBUG})
endif(WIN32)

if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
	add_library(${LIBNAME} SHARED ${SOURCES} ${HEADERS})
    set_target_properties(ftcommon PROPERTIES COMPILE_FLAGS "-fPIC")
endif (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
