cmake_minimum_required(VERSION 2.8.8) 
project(ftconfiguration CXX)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
message("${CMAKE_MODULE_PATH}")

set(Boost_USE_STATIC_LIBS       ON)
set(Boost_USE_MULTITHREADED     ON)
set(Boost_USE_STATIC_RUNTIME    OFF)

set(BOOST_ROOT $ENV{BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
set(BOOST_INCLUDEDIR ${BOOST_ROOT}/Include)
set(BOOST_LIBRARYDIR ${BOOST_ROOT}/lib)

include(common)
find_package(XercesC REQUIRED) # XSD DEPENDS ON ${XERCESC_FOUND}
if(XERCESC_FOUND)
  message(STATUS "Found Xerces-C: ${XERCESC_LIBRARIES}")
  message(STATUS "              : ${XERCESC_INCLUDE_DIR}")
  message(STATUS "       Version: ${XERCESC_VERSION}")
else(XERCESC_FOUND)
  message(FATAL_ERROR "The package Apache Xerces-C++ has not been found")
endif(XERCESC_FOUND)

include_directories(${XERCESC_INCLUDE_DIR})

find_package(pugixml REQUIRED)
find_package(Xsd REQUIRED) # CODESYNTHESIS
if(XSD_FOUND)
  message(STATUS "Package CodeSynthesis XSD found: ${XSD_INCLUDE_DIR}")
else(XSD_FOUND)
  message(FATAL_ERROR "The package CodeSynthesis XSD has not been found")
endif(XSD_FOUND)  
include_directories(${XSD_INCLUDE_DIR})
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   FaultTreeImport.cpp
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
)
set(HEADERS
   ${HEADERS}
   FaultTreeImport.h
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
)

include_directories(${Boost_INCLUDE_DIRS})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

set(FAULTTREE_XSD faulttree.xsd)
set(FAULTTREE_OUT ${CMAKE_CURRENT_SOURCE_DIR})
XSD_SCHEMA(FAULTTREE_XSD FAULTTREE_OUT)

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