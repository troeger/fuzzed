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

find_package(Boost COMPONENTS system filesystem program_options REQUIRED)
message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")
find_package(pugixml REQUIRED)

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
include_directories(${PUGIXML_INCLUDE_DIR})

find_package(pugixml REQUIRED)
find_package(Xsd REQUIRED) # CODESYNTHESIS
if(XSD_FOUND)
  message(STATUS "Package CodeSynthesis XSD found: ${XSD_INCLUDE_DIR}")
else(XSD_FOUND)
  message(FATAL_ERROR "The package CodeSynthesis XSD has not been found")
endif(XSD_FOUND)  
include_directories(${XSD_INCLUDE_DIR})
                                                                                                                                                                                                                        
set(SOURCES
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
   FaultTree.cpp
   util.cpp
)
set(HEADERS
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
   FaultTree.h
   platform.h
   util.h
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdParty)

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faultTree.xsd")

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

# TODO: in order not to re-generate all the time we actually want something like this (not working -.-):
# set(FAULTTREE_SRC "${CMAKE_CURRENT_SOURCE_DIR}/FaultTree.cpp")
# set(FAULTTREE_H "${CMAKE_CURRENT_SOURCE_DIR}/FaultTree.h")
# add_custom_command(
#   OUTPUT ${FAULTTREE_SRC} ${FAULTTREE_H}
#   DEPENDS ${FAULTTREE_XSD}
#   COMMAND ${XSD_EXECUTABLE}
#   ARGS cxx-tree --namespace-map net.faulttree=ft --hxx-suffix .h --cxx-suffix .cpp --output-dir ${CMAKE_CURRENT_SOURCE_DIR} ${FAULTTREE_XSD}
#   COMMENT "Generating C++ / XML mapping files"
#   VERBATIM)

set(XSD_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
  --generate-inline			#simple functions are inlined
  --root-element "FuzzTree"
  --type-naming ucc --function-naming lcc
  #--suppress-parsing 
  --generate-serialization --namespace-map net.faulttree=ft 
  --hxx-suffix .h --cxx-suffix .cpp

)

add_custom_command(
  TARGET ftconfiguration
  DEPENDS ${FAULTTREE_XSD}
  COMMAND ${XSD_EXECUTABLE}
  ARGS cxx-tree ${XSD_ARGS} --output-dir ${CMAKE_CURRENT_SOURCE_DIR} ${FAULTTREE_XSD}
  COMMENT "Generating C++ / XML mapping files"
  VERBATIM)