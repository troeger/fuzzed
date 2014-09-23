###################
# Generic settings
###################
project(FuzzedBackend)
cmake_minimum_required(VERSION 2.8.7)

# Load some additional CMake find... scripts 
SET (CMAKE_MODULE_PATH              "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# Store all binary output in /lib
SET (CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib")
SET (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib")
SET (CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib")

# Get some symbold for GDB
SET (CMAKE_BUILD_TYPE Debug)

############################################################################
# Platform-specific compilation behavior
############################################################################
if(WIN32)
	set(Boost_USE_STATIC_LIBS ON)
	set(USE_OMP ON)
elseif(UNIX)
	set(USE_OMP ON)
endif()

if (USE_OMP)
	add_definitions(-DOMP_PARALLELIZATION=1)
endif() 

############################################################################
# Compiler-specific compilation behavior
############################################################################

if (CMAKE_COMPILER_IS_GNUCC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lpthread -std=c++0x -fPIC -fexceptions -Wno-deprecated-declarations -fpermissive")
elseif (MSVC)
	if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
		string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
	else()
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
	endif()
	add_definitions(/D_CRT_SECURE_NO_WARNINGS /DNOMINMAX /DWIN32_LEAN_AND_MEAN)
	set(TPN_WIN32 "${TPN_WIN32} /EHsc")
else()
	message(WARNING "Untested compiler") # TODO see if we can support clang too
endif()

################# BOOST #################
#########################################

add_definitions(-DBOOST_DATE_TIME_NO_LIB -DBOOST_REGEX_NO_LIB)
add_definitions(-D_ALLOW_KEYWORD_MACROS)

set(BOOST_ROOT $ENV{BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
set(BOOST_INCLUDEDIR ${BOOST_ROOT}/Include)
set(BOOST_LIBRARYDIR ${BOOST_ROOT}/lib)

set(Boost_DIR ${BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
find_package(Boost 1.48 COMPONENTS
	graph
	date_time
	system
	filesystem
	program_options
REQUIRED)

message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")

############### PUGI ####################
#########################################

add_subdirectory(thirdParty/pugixml)
message("Building pugixml")
set(PUGIXML_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/thirdParty/pugixml/src")

################# Directories ###########
#########################################

#TODO: From here on, the common subproject and general stuff gets intermixed
#      Try to make 'common' a self-hosted compilation unit as the others

include_directories(
	${PUGIXML_INCLUDE_DIR}
	${Boost_INCLUDE_DIRS}
	${CMAKE_CURRENT_SOURCE_DIR}/fuzztreeconfiguration
	${CMAKE_CURRENT_SOURCE_DIR}/model
	${CMAKE_CURRENT_SOURCE_DIR}/common
	${CMAKE_CURRENT_SOURCE_DIR}/thirdParty
)

set(COMMON_DIR 		${CMAKE_CURRENT_SOURCE_DIR}/common)
set(MODEL_DIR 		${CMAKE_CURRENT_SOURCE_DIR}/model)

############### COMMON ##################
#########################################

set(COMMON_SOURCES
	${MODEL_DIR}/Model.cpp
	${MODEL_DIR}/Node.cpp
	${MODEL_DIR}/Probability.cpp

	${COMMON_DIR}/util.cpp

	${COMMON_DIR}/CommandLineParser.cpp
	${COMMON_DIR}/Issue.cpp
	${COMMON_DIR}/FatalException.cpp
	${COMMON_DIR}/DeadlockMonitor.cpp
)

set(COMMON_HEADERS
	${MODEL_DIR}/Model.h
	${MODEL_DIR}/Node.h
	${MODEL_DIR}/Probability.h

	${COMMON_DIR}/platform.h
	${COMMON_DIR}/util.h
	${COMMON_DIR}/resultxml.h

	${COMMON_DIR}/CommandLineParser.h
	${COMMON_DIR}/Issue.h
	${COMMON_DIR}/FatalException.h
	${COMMON_DIR}/DeadlockMonitor.h
	${COMMON_DIR}/Dynamic2dArray.h
)

add_library(common_model STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})

include_directories(${COMMON_DIR})
target_link_libraries(common_model ${Boost_LIBRARIES} ${PUGIXML_LIB})

add_subdirectory(fuzztreeconfiguration)
add_subdirectory(fuzztreeanalysis)
add_subdirectory(simulation)
add_subdirectory(mincut)

add_executable(common_model_test test_common_model.cpp 
	${MODEL_DIR}/Model.cpp
	${MODEL_DIR}/Node.cpp
	${MODEL_DIR}/Model.h
	${MODEL_DIR}/Node.h
	${MODEL_DIR}/Probability.h
	${MODEL_DIR}/Probability.cpp
	${MODEL_DIR}/NumericInterval.h

	${COMMON_DIR}/Issue.h
	${COMMON_DIR}/FatalException.h
	${COMMON_DIR}/Issue.cpp
	${COMMON_DIR}/FatalException.cpp
	${COMMON_DIR}/util.cpp
	${COMMON_DIR}/util.h

	fuzztreeconfiguration/FuzzTreeConfiguration.cpp
	fuzztreeconfiguration/FuzzTreeConfiguration.h
	fuzztreeconfiguration/FuzzTreeToFaultTree.cpp
	fuzztreeconfiguration/FuzzTreeToFaultTree.h
)
target_link_libraries(common_model_test ${Boost_LIBRARIES} ${PUGIXML_LIB})