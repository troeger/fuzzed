cmake_minimum_required(VERSION 2.8.8) 

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set(Boost_USE_STATIC_LIBS       ON)
set(Boost_USE_MULTITHREADED     ON)
set(Boost_USE_STATIC_RUNTIME    OFF)
#add_definitions(-DBOOST_ALL_NO_LIB)
#add_definitions(-DBoost_DEBUG=1)

set(BOOST_ROOT $ENV{BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
set(BOOST_INCLUDEDIR ${BOOST_ROOT}/Include)
set(BOOST_LIBRARYDIR ${BOOST_ROOT}/lib)
       
set(FT_CONFIG_DIR "${PROJECT_SOURCE_DIR}/../fuzztreeconfiguration")
find_package(ftconfiguration REQUIRED)

set(FT_LIB_DIR "${PROJECT_SOURCE_DIR}/lib")
set(FT_INCLUDE_DIR
	"${PROJECT_SOURCE_DIR}/modeltransform"
	"${PROJECT_SOURCE_DIR}/simulation" 
	"${PROJECT_SOURCE_DIR}/common"
	"${PROJECT_SOURCE_DIR}/fuzztreeconfiguration"
	"${PROJECT_SOURCE_DIR}/thirdParty")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/lib")

# so the shared libs can see symbols from static libs
#set(CMAKE_SHARED_LINKER_FLAGS "-Wl,--export-all-symbols")

if(MSVC)
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
  else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
  endif()
  add_definitions(/D_CRT_SECURE_NO_WARNINGS /DNOMINMAX /DWIN32_LEAN_AND_MEAN)
elseif(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pedantic -std=c++0x -fPIC")
  set(Boost_USE_STATIC_LIBS OFF)
endif()

set(Boost_DIR ${BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
find_package(Boost COMPONENTS system filesystem program_options REQUIRED)
message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")
find_package(pugixml REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_CONFIG_INCLUDE})
link_directories(${Boost_LIBRARY_DIRS})

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

find_package(beanstalkpp REQUIRED)
message(STATUS "Found Beanstalk Client lib: ${BEANSTALKPP_LIB}")
include_directories(${BEANSTALKPP_INCLUDE})

option(BUILD_SIMULATION_EXECUTABLE ON)
option(USE_TIMENET ON)

option(BUILD_TESTS OFF)
if (${BUILD_TESTS})
	find_package(gtest REQUIRED)
	add_subdirectory(tests)
	message("Building Tests")
endif()

add_subdirectory(common)
add_subdirectory(modeltransform)
add_subdirectory(simulation)