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
	 set(USE_INTEL_COMPILER OFF) 
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
	${CMAKE_CURRENT_SOURCE_DIR}/common_generated
	${CMAKE_CURRENT_SOURCE_DIR}/thirdParty
)

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/common)
set(COMMON_GEN_DIR ${CMAKE_CURRENT_SOURCE_DIR}/common_generated)

############### XSD COMPILER ############
#########################################

set(XSD_FILE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../FuzzEd/static/xsd")

set(XSD_GENERATED_TREE_FILES
	${COMMON_GEN_DIR}/fuzztree.h
	${COMMON_GEN_DIR}/faulttree.h
	${COMMON_GEN_DIR}/fuzztree.cpp
	${COMMON_GEN_DIR}/faulttree.cpp)

set(FAULTTREE_XSD "${XSD_FILE_PATH}/faulttree.xsd")
set(FUZZTREE_XSD  "${XSD_FILE_PATH}/fuzztree.xsd")

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
	${COMMON_GEN_DIR}/backendResult.h
	${COMMON_GEN_DIR}/commonTypes.h
	${COMMON_GEN_DIR}/configurations.h
	${COMMON_GEN_DIR}/backendResult.cpp
	${COMMON_GEN_DIR}/commonTypes.cpp
	${COMMON_GEN_DIR}/configurations.cpp)

set(RESULT_XSD					"${XSD_FILE_PATH}/backendResult.xsd")
set(COMMON_TYPES_XSD			"${XSD_FILE_PATH}/commonTypes.xsd")
set(CONFIGURATION_XSD			"${XSD_FILE_PATH}/configurations.xsd")

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
			--output-dir ${COMMON_GEN_DIR}
			${COMMON_TYPES_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_RESULT_ARGS}
			--output-dir ${COMMON_GEN_DIR}
			--root-element "backendResults"
			${RESULT_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_RESULT_ARGS}
			--output-dir ${COMMON_GEN_DIR}
			${CONFIGURATION_XSD}

	COMMAND ${XSD_EXECUTABLE}
		cxx-tree 
			${XSD_TO_FAULTTREE_ARGS} 
			${TREE_CUSTOMIZATION_ARGS}
			--output-dir ${COMMON_GEN_DIR}
			${FAULTTREE_XSD}

	COMMAND ${XSD_EXECUTABLE} 
		cxx-tree
			${XSD_TO_FUZZTREE_ARGS}
			${FUZZTREE_CUSTOMIZATION_ARGS}
			--output-dir ${COMMON_GEN_DIR}
			${FUZZTREE_XSD}

	COMMENT "Generating C++ / XML mapping files"
	VERBATIM

	DEPENDS ${COMMON_TYPES_XSD} ${RESULT_XSD} ${CONFIGURATION_XSD} ${FAULTTREE_XSD} ${FUZZTREE_XSD})

############### COMMON ##################
#########################################

set(COMMON_SOURCES
	${COMMON_DIR}/util.cpp
	${COMMON_DIR}/xmlutil.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp

	${COMMON_DIR}/CommandLineParser.cpp
	${COMMON_DIR}/FaultTreeToFuzzTree.cpp
	${COMMON_DIR}/Issue.cpp
	${COMMON_DIR}/FatalException.cpp
	${COMMON_DIR}/DeadlockMonitor.cpp

	${COMMON_GEN_DIR}/faulttree.cpp
	${COMMON_GEN_DIR}/fuzztree.cpp
	${COMMON_GEN_DIR}/backendResult.cpp
	${COMMON_GEN_DIR}/commonTypes.cpp
	${COMMON_GEN_DIR}/configurations.cpp
)

set(COMMON_HEADERS
	${COMMON_DIR}/platform.h
	${COMMON_DIR}/util.h
	${COMMON_DIR}/xmlutil.h
	${COMMON_DIR}/FaultTreeTypes.h
	${COMMON_DIR}/FuzzTreeTypes.h

	${COMMON_DIR}/CommandLineParser.h
	${COMMON_DIR}/FaultTreeToFuzzTree.h
	${COMMON_DIR}/Issue.h
	${COMMON_DIR}/FatalException.h
	${COMMON_DIR}/DeadlockMonitor.h
	${COMMON_DIR}/Dynamic2dArray.h

	${COMMON_GEN_DIR}/faulttree.h
	${COMMON_GEN_DIR}/fuzztree.h
	${COMMON_GEN_DIR}/backendResult.h
	${COMMON_GEN_DIR}/commonTypes.h
	${COMMON_GEN_DIR}/configurations.h
)

add_library(common_model STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})
target_link_libraries(common_model ${XERCESC_LIBRARIES} ${Boost_LIBRARIES} ${PUGIXML_LIB})

############### UNIT TESTS ##############
#########################################

add_subdirectory(fuzztreeconfiguration)
add_subdirectory(fuzztreeanalysis)
add_subdirectory(simulation)
add_subdirectory(mincut)