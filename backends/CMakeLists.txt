####################################################################################################
# Overwriting the default compiler is a bad thing:
# http://www.cmake.org/Wiki/CMake_FAQ
# It must be done before the project definition.
#
# We only need this for Mac's, were Codesynthesis
# cannot deal with the default CLang compiler.
# A manual switch to g++ is therefore needed by calling:
# cmake -D CMAKE_C_COMPILER=/usr/local/bin/gcc-4.9 -D CMAKE_CXX_COMPILER=/usr/local/bin/g++-4.9 .
####################################################################################################

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


############################################################################
# Platform-specific compilation behavior
############################################################################
if(APPLE)
	# Homebrew on Mac OS X has no Codesynthesis XSD available, so we use our own copy
	set(XSD_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/thirdParty/xsd_apple/libxsd/)
	set(XSD_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}/thirdParty/xsd_apple/bin/xsd)
elseif(WIN32)
	 set(Boost_USE_STATIC_LIBS ON)
	 add_definitions(-DOMP_PARALLELIZATION=1)
elseif(UNIX)
	 set(USE_INTEL_COMPILER OFF) 
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
	date_time
	system
	filesystem
	program_options
REQUIRED)

message(STATUS "** Boost Libraries: ${Boost_LIBRARIES}")

################# XSD ###################
#########################################

find_package(XercesC REQUIRED) # XSD DEPENDS ON ${XERCESC_FOUND}
if(XERCESC_FOUND)
	message(STATUS "Found Xerces-C: ${XERCESC_LIBRARIES}")
	message(STATUS "              : ${XERCESC_INCLUDE_DIR}")
	message(STATUS "       Version: ${XERCESC_VERSION}")
else(XERCESC_FOUND)
	message(FATAL_ERROR "The package Apache Xerces-C++ has not been found")
endif(XERCESC_FOUND)

find_package(Xsd REQUIRED) # CODESYNTHESIS
if(XSD_FOUND)
	message(STATUS "Package CodeSynthesis XSD found: ${XSD_INCLUDE_DIR}")
else(XSD_FOUND)
	message(FATAL_ERROR "The package CodeSynthesis XSD has not been found")
endif(XSD_FOUND)  

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
	${XERCESC_INCLUDE_DIR}
	${XSD_INCLUDE_DIR}
	${PUGIXML_INCLUDE_DIR}
	${Boost_INCLUDE_DIRS}
	${CMAKE_CURRENT_SOURCE_DIR}/fuzztreeconfiguration
	${CMAKE_CURRENT_SOURCE_DIR}/common
	${CMAKE_CURRENT_SOURCE_DIR}/thirdParty
)

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/common)

############### XSD COMPILER ############
#########################################

set(XSD_GENERATED_TREE_FILES
	${COMMON_DIR}/fuzztree.h
	${COMMON_DIR}/faulttree.h
	${COMMON_DIR}/fuzztree.cpp
	${COMMON_DIR}/faulttree.cpp)

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faulttree.xsd")
set(FUZZTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/fuzztree.xsd")
set(TREE_SCHEMAS ${FAULTTREE_XSD} ${FUZZTREE_XSD})

########### FAULT TREE MODEL ############

set(XSD_TO_FAULTTREE_ARGS
	--include-with-brackets #include with <> instead of ""
	--generate-polymorphic  #needed for xsi:type
	--polymorphic-type-all
	--root-element "FaultTree"
	--type-naming ucc
	--function-naming lcc
	--generate-serialization
	--namespace-map net.faulttree=faulttree
	--generate-forward
	--hxx-suffix .h
	--cxx-suffix .cpp
)

set(XSD_TO_FUZZTREE_ARGS
	--include-with-brackets #include with <> instead of ""
	--generate-polymorphic  #needed for xsi:type
	--polymorphic-type-all
	--root-element "FuzzTree"
	--type-naming ucc 
	--function-naming lcc
	--generate-serialization
	--namespace-map net.fuzztree=fuzztree 
	--generate-forward
	--hxx-suffix .h
	--cxx-suffix .cpp
)

########### RESULT XML ##################

set(XSD_GENERATED_RESULT_FILES
	${COMMON_DIR}/analysisResult.h
	${COMMON_DIR}/simulationResult.h
	${COMMON_DIR}/configurationResult.h
	${COMMON_DIR}/commonTypes.h
	${COMMON_DIR}/configurations.h
	${COMMON_DIR}/analysisResult.cpp
	${COMMON_DIR}/simulationResult.cpp
	${COMMON_DIR}/configurationResult.cpp
	${COMMON_DIR}/commonTypes.cpp
	${COMMON_DIR}/configurations.cpp)

set(ANALYSIS_RESULT_XSD			"${CMAKE_CURRENT_SOURCE_DIR}/xml/analysisResult.xsd")
set(SIMULATION_RESULT_XSD		"${CMAKE_CURRENT_SOURCE_DIR}/xml/simulationResult.xsd")
set(CONFIGURATION_RESULT_XSD	"${CMAKE_CURRENT_SOURCE_DIR}/xml/configurationResult.xsd")
set(COMMON_TYPES_XSD			"${CMAKE_CURRENT_SOURCE_DIR}/xml/commonTypes.xsd")
set(CONFIGURATION_XSD			"${CMAKE_CURRENT_SOURCE_DIR}/xml/configurations.xsd")

set(XSD_RESULT_ARGS
	--include-with-brackets #include with <> instead of ""
	--generate-polymorphic  #needed for xsi:type
	--polymorphic-type-all
	--type-naming ucc
	--function-naming lcc
	--generate-serialization
	--hxx-suffix .h
	--cxx-suffix .cpp
)

########### CODE GENERATION ################

add_custom_command(OUTPUT ${XSD_GENERATED_RESULT_FILES} ${XSD_GENERATED_TREE_FILES}
	
	COMMAND ${XSD_EXECUTABLE}
		cxx-tree 
			${XSD_RESULT_ARGS} 
			--output-dir ${COMMON_DIR}
			${COMMON_TYPES_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_RESULT_ARGS}
			--output-dir ${COMMON_DIR}
			${CONFIGURATION_XSD}

	COMMAND ${XSD_EXECUTABLE}
		cxx-tree 
			${XSD_RESULT_ARGS} 
			--output-dir ${COMMON_DIR}
			--root-element "analysisResults"
			${ANALYSIS_RESULT_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_RESULT_ARGS}
			--output-dir ${COMMON_DIR}
			--root-element "configurationResults"
			${CONFIGURATION_RESULT_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_RESULT_ARGS}
			--output-dir ${COMMON_DIR}
			--root-element "simulationResults"
			${SIMULATION_RESULT_XSD}

	COMMAND ${XSD_EXECUTABLE}
		cxx-tree 
			${XSD_TO_FAULTTREE_ARGS} 
			${TREE_CUSTOMIZATION_ARGS}
			--output-dir ${COMMON_DIR}
			${FAULTTREE_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_TO_FUZZTREE_ARGS}
			${FUZZTREE_CUSTOMIZATION_ARGS}
			--output-dir ${COMMON_DIR}
			${FUZZTREE_XSD}

	COMMENT "Generating C++ / XML mapping files"
	VERBATIM)

############### COMMON ##################
#########################################

set(COMMON_SOURCES
	${COMMON_DIR}/util.cpp
	${COMMON_DIR}/xmlutil.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp
	${COMMON_DIR}/faulttree.cpp
	${COMMON_DIR}/fuzztree.cpp
	${COMMON_DIR}/analysisResult.cpp
	${COMMON_DIR}/simulationResult.cpp
	${COMMON_DIR}/configurationResult.cpp
	${COMMON_DIR}/commonTypes.cpp
	${COMMON_DIR}/configurations.cpp
	${COMMON_DIR}/CommandLineParser.cpp
)

set(COMMON_HEADERS
	${COMMON_DIR}/platform.h
	${COMMON_DIR}/util.h
	${COMMON_DIR}/xmlutil.h
	${COMMON_DIR}/FaultTreeTypes.h
	${COMMON_DIR}/FuzzTreeTypes.h
	${COMMON_DIR}/faulttree.h
	${COMMON_DIR}/fuzztree.h
	${COMMON_DIR}/analysisResult.h
	${COMMON_DIR}/simulationResult.h
	${COMMON_DIR}/configurationResult.h
	${COMMON_DIR}/commonTypes.h
	${COMMON_DIR}/configurations.h
	${COMMON_DIR}/CommandLineParser.h
)

add_library(common_model STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})
target_link_libraries(common_model ${XERCESC_LIBRARIES} ${Boost_LIBRARIES} ${PUGIXML_LIB})

############### UNIT TESTS ##############
#########################################

# builds some very basic low-level white box tests
# requires Googletest
set(BUILD_TESTS OFF)
if (${BUILD_TESTS})
	find_package(gtest REQUIRED)
	add_subdirectory(tests)
	message("Building Tests")
endif()

add_subdirectory(fuzztreeconfiguration)
add_subdirectory(fuzztreeanalysis)
add_subdirectory(simulation)