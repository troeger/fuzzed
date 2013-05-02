cmake_minimum_required(VERSION 2.8.8) 

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set(Boost_USE_STATIC_LIBS       OFF)
set(Boost_USE_MULTITHREADED     ON)
set(Boost_USE_STATIC_RUNTIME    OFF)
#add_definitions(-DBOOST_ALL_NO_LIB)
#add_definitions(-DBoost_DEBUG=1)

set(BOOST_ROOT $ENV{BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
set(BOOST_INCLUDEDIR ${BOOST_ROOT}/Include)
set(BOOST_LIBRARYDIR ${BOOST_ROOT}/lib)
       
set(FT_LIB_DIR "${PROJECT_SOURCE_DIR}/lib")
set(FT_INCLUDE_DIR 
	"${PROJECT_SOURCE_DIR}/modeltransform" 
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
  ADD_DEFINITIONS(/D_CRT_SECURE_NO_WARNINGS /DNOMINMAX /DWIN32_LEAN_AND_MEAN)
elseif(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pedantic -std=c++0x -fPIC")
endif()

set(Boost_DIR ${BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)

find_package(Boost COMPONENTS filesystem program_options REQUIRED)
message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")
find_package(pugixml REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

option(BUILD_TESTS OFF)
if (${BUILD_TESTS})
	find_package(gtest REQUIRED)
	add_subdirectory(tests)
	message("Building Tests")
endif()

add_subdirectory(common)

add_subdirectory(modeltransform)
option(BUILD_SIMULATION_EXECUTABLE ON)
add_subdirectory(fuzztreeconfiguration)
add_subdirectory(simulation)
