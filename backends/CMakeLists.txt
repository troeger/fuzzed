set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
option(VARIADIC_TEMPLATES OFF) # switch on to use Visitor pattern. Work in progress.

if(APPLE)
	message("This is Apple, expecting GCC-4.9 and library installations.")
	# Mac OS X specific code
	set(CMAKE_CXX_FLAGS "-std=c++11")
	set(CMAKE_C_COMPILER "gcc-4.9")
	set(CMAKE_CXX_COMPILER "gcc-4.9")
	set(CMAKE_INCLUDE_PATH "/usr/local/include/")
	set(XSD_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../tools/xsdcompile/include/)
	set(XSD_EXECUTABLE ${CMAKE_CURRENT_SOURCE_DIR}"../tools/xsdcompile/bin/xsd")
	set(BUILD_PUGIXML ON)
elseif(WIN32)
	 message("This is Windows.")
	 set(BUILD_PUGIXML ON)
	 set(Boost_USE_STATIC_LIBS ON)
elseif(UNIX)
	 message("This is Linux.")
	 set(USE_INTEL_COMPILER OFF) 
	 set(BUILD_PUGIXML ON)
endif() 

project(FuzztreeBackends)
cmake_minimum_required(VERSION 2.8.7)
set(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake")

# All libraries should end up in the same directory
set(FT_LIB_DIR "${PROJECT_SOURCE_DIR}/lib")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${FT_LIB_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${FT_LIB_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${FT_LIB_DIR})
set(CMAKE_EXECUTABLE_OUTPUT_DIRECTORY ${FT_LIB_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${FT_LIB_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${FT_LIB_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${FT_LIB_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${FT_LIB_DIR})
set(CMAKE_EXECUTABLE_OUTPUT_DIRECTORY_RELEASE ${FT_LIB_DIR})
set(CMAKE_EXECUTABLE_OUTPUT_DIRECTORY_DEBUG ${FT_LIB_DIR})

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
	message("Unsupported compiler") # TODO see if we can support clang too
endif()

################# BOOST #################
#########################################

add_definitions(-DBOOST_DATE_TIME_NO_LIB -DBOOST_REGEX_NO_LIB)
add_definitions(-D_ALLOW_KEYWORD_MACROS)

set(BOOST_ROOT $ENV{BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
set(BOOST_INCLUDEDIR ${BOOST_ROOT}/Include)
set(BOOST_LIBRARYDIR ${BOOST_ROOT}/lib)

set(Boost_DIR ${BOOST_ROOT} CACHE STRING "Set the value of BOOST_ROOT to point to the root folder of your boost install." FORCE)
find_package(Boost 1.51.0 COMPONENTS # TODO find out which version is really required. Maybe 1.50 would suffice too.
	date_time
	system
	filesystem
	program_options
	exception
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

if(BUILD_PUGIXML)
	add_subdirectory(thirdParty/pugixml)
	message("Building pugixml")
	if(WIN32)
		set(PUGIXML_LIB "${FT_LIB_DIR}/pugixml.lib")
	else(WIN32)#TODO
		set(PUGIXML_LIB "${FT_LIB_DIR}/libpugixml.a")
	endif(WIN32)
	set(PUGIXML_INCLUDE_DIR thirdParty/pugixml/src)
else()
	find_package(pugixml REQUIRED)
	message(STATUS "Found Pugixml lib: ${PUGIXML_LIB}")
endif()

################# Directories ###########
#########################################

include_directories(
	${XERCESC_INCLUDE_DIR}
	${XSD_INCLUDE_DIR}
	${PUGIXML_INCLUDE_DIR}
	${Boost_INCLUDE_DIRS}
	${CMAKE_CURRENT_SOURCE_DIR}/thirdParty
	${CMAKE_CURRENT_SOURCE_DIR}/fuzztreeconfiguration
	${CMAKE_CURRENT_SOURCE_DIR}/common
)

set(COMMON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/common)

############### XSD COMPILER ############
#########################################

set(XSD_GENERATED_FILES
	${COMMON_DIR}/fuzztree.h
	${COMMON_DIR}/faulttree.h
	${COMMON_DIR}/fuzztree.cpp
	${COMMON_DIR}/faulttree.cpp)

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faulttree.xsd")
set(FUZZTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/fuzztree.xsd")
set(SCHEMAS ${FAULTTREE_XSD} ${FUZZTREE_XSD})

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

if (VARIADIC_TEMPLATES)
	# the following options, which generate a tree visitor, need C++0x support for variadic templates
	# GCC >= 4.7 and Intel 13.0 support it, but not VS2012...

	set(TREE_CUSTOMIZATION_ARGS
		--custom-type Node=FaultTreeVisitable<Node_base>/Node_base
		--custom-type TopEvent=FaultTreeVisitable<TopEvent_base>/TopEvent_base
		--custom-type BasicEvent=FaultTreeVisitable<BasicEvent_base>/BasicEvent_base
		--custom-type HouseEvent=FaultTreeVisitable<HouseEvent_base>/HouseEvent_base
		--custom-type UndevelopedEvent=FaultTreeVisitable<UndevelopedEvent_base>/UndevelopedEvent_base
		--custom-type IntermediateEvent=FaultTreeVisitable<IntermediateEvent_base>/IntermediateEvent_base
		--custom-type ChildNode=FaultTreeVisitable<ChildNode_base>/ChildNode_base
		--custom-type Gate=FaultTreeVisitable<Gate_base>/Gate_base
		--custom-type And=FaultTreeVisitable<And_base>/And_base
		--custom-type Or=FaultTreeVisitable<Or_base>/Or_base
		--custom-type Xor=FaultTreeVisitable<Xor_base>/Xor_base
		--custom-type VotingOr=FaultTreeVisitable<VotingOr_base>/VotingOr_base
		--custom-type DynamicGate=FaultTreeVisitable<DynamicGate_base>/DynamicGate_base
		--custom-type Spare=FaultTreeVisitable<Spare_base>/Spare_base
		--custom-type FDEP=FaultTreeVisitable<FDEP_base>/FDEP_base
		--custom-type Sequence=FaultTreeVisitable<Sequence_base>/Sequence_base
		--custom-type PriorityAnd=FaultTreeVisitable<PriorityAnd_base>/PriorityAnd_base
	--fwd-prologue "#include <Visitable.h>"
	)

	set(FUZZTREE_CUSTOMIZATION_ARGS
		--custom-type Node=FuzzTreeVisitable<Node_base>/Node_base
		--custom-type TopEvent=FuzzTreeVisitable<TopEvent_base>/TopEvent_base
		--custom-type BasicEvent=FuzzTreeVisitable<BasicEvent_base>/BasicEvent_base
		--custom-type HouseEvent=FuzzTreeVisitable<HouseEvent_base>/HouseEvent_base
		--custom-type UndevelopedEvent=FuzzTreeVisitable<UndevelopedEvent_base>/UndevelopedEvent_base
		--custom-type IntermediateEvent=FuzzTreeVisitable<IntermediateEvent_base>/IntermediateEvent_base
		--custom-type ChildNode=FuzzTreeVisitable<ChildNode_base>/ChildNode_base
		--custom-type Gate=FuzzTreeVisitable<Gate_base>/Gate_base
		--custom-type And=FuzzTreeVisitable<And_base>/And_base
		--custom-type Or=FuzzTreeVisitable<Or_base>/Or_base
		--custom-type Xor=FuzzTreeVisitable<Xor_base>/Xor_base
		--custom-type VotingOr=FuzzTreeVisitable<VotingOr_base>/VotingOr_base
		--custom-type DynamicGate=FuzzTreeVisitable<DynamicGate_base>/DynamicGate_base
		--custom-type Spare=FuzzTreeVisitable<Spare_base>/Spare_base
		--custom-type FDEP=FuzzTreeVisitable<FDEP_base>/FDEP_base
		--custom-type Sequence=FuzzTreeVisitable<Sequence_base>/Sequence_base
		--custom-type PriorityAnd=FuzzTreeVisitable<PriorityAnd_base>/PriorityAnd_base
		--custom-type RedundancyVariationPoint=FuzzTreeVisitable<RedundancyVariationPoint_base>/RedundancyVariationPoint_base
		--custom-type FeatureVariationPoint=FuzzTreeVisitable<FeatureVariationPoint_base>/FeatureVariationPoint_base
		--custom-type VariationPoint=FuzzTreeVisitable<VariationPoint_base>/VariationPoint_base
		--custom-type IntermediateEventSet=FuzzTreeVisitable<IntermediateEventSet_base>/IntermediateEventSet_base
		--custom-type BasicEventSet=FuzzTreeVisitable<BasicEventSet_base>/BasicEventSet_base
	--fwd-prologue "#include <Visitable.h>"
	)

endif(VARIADIC_TEMPLATES)

add_custom_command(OUTPUT ${XSD_GENERATED_FILES}
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

add_definitions(-DFUZZTREEXSD="${FUZZTREE_XSD}")
add_definitions(-DFAULTTREEXSD="${FAULTTREE_XSD}")

############### COMMON ##################
#########################################

set(COMMON_SOURCES
	${COMMON_DIR}/util.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp
	${COMMON_DIR}/FaultTreeTypes.cpp
	${COMMON_DIR}/FuzzTreeTypes.cpp
	${COMMON_DIR}/faulttree.cpp
	${COMMON_DIR}/fuzztree.cpp
)

set(COMMON_HEADERS
	${COMMON_DIR}/platform.h
	${COMMON_DIR}/util.h
	${COMMON_DIR}/FaultTreeTypes.h
	${COMMON_DIR}/FuzzTreeTypes.h
	${COMMON_DIR}/faulttree.h
	${COMMON_DIR}/fuzztree.h
)

set(COMMON_LINKED_LIBS
	${XERCESC_LIBRARIES}
	${Boost_LIBRARIES}
	${PUGIXML_LIB})
message("${COMMON_LINKED_LIBS}")
add_library(common_model STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})
target_link_libraries(common_model ${COMMON_LINKED_LIBS})
set(COMMON_LINKED_LIBS
	${COMMON_LINKED_LIBS}
	common_model)

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