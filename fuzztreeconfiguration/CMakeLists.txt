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

foreach(OUTPUTCONFIG ${CMAKE_CONFIGURATION_TYPES})
    string(TOUPPER ${OUTPUTCONFIG} OUTPUTCONFIG)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/bin)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/lib)
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${OUTPUTCONFIG} ${PROJECT_SOURCE_DIR}/lib)
endforeach(OUTPUTCONFIG CMAKE_CONFIGURATION_TYPES)

find_package(Boost COMPONENTS system filesystem program_options REQUIRED)
message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")

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
   TreeHelpers.cpp
   TransformUtil.cpp
   main.cpp
   faulttree.cpp
   fuzztree.cpp
   #fuzztree_custom.cpp # custom methods. not generated.
)
set(HEADERS
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
   TreeHelpers.h
   TransformUtil.h
   platform.h
   faulttree.h
   fuzztree.h
   FaultTreeTypes.h
   FuzzTreeTypes.h
   #fuzztree_custom.h # custom methods. not generated.
)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/thirdParty)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faulttree.xsd")
set(FUZZTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/fuzztree.xsd")

set(SCHEMAS ${FAULTTREE_XSD} ${FUZZTREE_XSD})

add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS} ${SCHEMAS})
target_link_libraries(ftconfiguration ${Boost_LIBRARIES} ${XERCESC_LIBRARIES})

option(BUILD_TEST_EXECUTABLE OFF)#just for testing
if (BUILD_TEST_EXECUTABLE)
  add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS} ${SCHEMAS})
  target_link_libraries(ftconfiguration_exe ${Boost_LIBRARIES} ${XERCESC_LIBRARIES})
endif(BUILD_TEST_EXECUTABLE)

set(XSD_TO_FAULTTREE_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
  --polymorphic-type-all
  --root-element "FaultTree"
  --type-naming ucc
  --function-naming lcc
  --generate-serialization
  --generate-from-base-ctor
  --namespace-map net.faulttree=faulttree
  --hxx-suffix .h --cxx-suffix .cpp
)

set(XSD_TO_FUZZTREE_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
  --polymorphic-type-all
  --root-element "FuzzTree"
  --type-naming ucc 
  --function-naming lcc
  --generate-serialization
  --generate-from-base-ctor
  --namespace-map net.fuzztree=fuzztree 
  --hxx-suffix .h --cxx-suffix .cpp
  # the following options enable custom class implementations, but it seems easier to write helpers by hand
  #--custom-type "Node=Node_impl<Node_base>/Node_base"
  #--custom-type "VotingOr=VotingOr_impl<VotingOr_base>/VotingOr_base"
  #--custom-type "BasicEvent=BasicEvent_impl<BasicEvent_base>/BasicEvent_base"
  #--custom-type "BasicEventSet=BasicEventSet_impl<BasicEventSet_base>/BasicEventSet_base"
  #--hxx-epilogue #include "fuzztree_custom.h"
)

add_custom_target(generateFaultTreeModel
  DEPENDS ${FAULTTREE_XSD}
  COMMAND ${XSD_EXECUTABLE} cxx-tree ${XSD_TO_FAULTTREE_ARGS} --output-dir ${CMAKE_CURRENT_SOURCE_DIR} ${FAULTTREE_XSD}
  COMMENT "Generating C++ / XML mapping files for FaultTrees"
  VERBATIM)

add_custom_target(generateFuzzTreeModel
  DEPENDS ${FUZZTREE_XSD}
  COMMAND ${XSD_EXECUTABLE} cxx-tree ${XSD_TO_FUZZTREE_ARGS} --output-dir ${CMAKE_CURRENT_SOURCE_DIR} ${FUZZTREE_XSD}
  COMMENT "Generating C++ / XML mapping files for FuzzTrees"
  VERBATIM)

add_definitions(-DFUZZTREEXSD="${FUZZTREE_XSD}")
add_definitions(-DFAULTTREEXSD="${FAULTTREE_XSD}")