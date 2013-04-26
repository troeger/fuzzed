project(ftconfiguration CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   FuzzTreeImport.cpp
   FuzzTreeTransform.cpp
)
set(HEADERS
   ${HEADERS}
   FuzzTreeImport.h
   FuzzTreeTransform.h
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS})

target_link_libraries(ftconfiguration ${Boost_LIBRARIES})
if (WIN32)
   target_link_libraries(ftconfiguration optimized ${PUGIXML_LIB_RELEASE})
   target_link_libraries(ftconfiguration debug ${PUGIXML_LIB_DEBUG})
endif(WIN32)

if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
   set_target_properties(ftcommon PROPERTIES COMPILE_FLAGS "-fPIC")
endif (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
