project(ftconfiguration CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   FuzzTreeImport.cpp
   FaultTreeImport.cpp
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
)
set(HEADERS
   ${HEADERS}
   FuzzTreeImport.h
   FaultTreeImport.h
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})
include_directories(${PUGIXML_INCLUDE_DIR})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

if (WIN32)
   add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS})
   target_link_libraries(ftconfiguration optimized ${PUGIXML_LIB_RELEASE})
   target_link_libraries(ftconfiguration debug ${PUGIXML_LIB_DEBUG})
endif(WIN32)

if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
   add_library(ftconfiguration SHARED ${SOURCES} ${HEADERS})
   set_target_properties(ftcommon PROPERTIES COMPILE_FLAGS "-fPIC")
endif (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
target_link_libraries(ftconfiguration ${Boost_LIBRARIES})