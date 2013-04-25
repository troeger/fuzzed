project(common)

set(SOURCES
	${SOURCES}
	
	util.cpp
	XMLImport.cpp
	Condition.cpp
)

set(HEADERS
	${HEADERS}
	
	util.h
	XMLImport.h
	Types.h
	Constants.h
	Condition.h
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})
add_library(ftcommon STATIC ${SOURCES} ${HEADERS})

if (WIN32)
	target_link_libraries(ftcommon optimized ${PUGIXML_LIB_RELEASE})
	target_link_libraries(ftcommon debug ${PUGIXML_LIB_DEBUG})
endif(WIN32)