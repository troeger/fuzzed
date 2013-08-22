set(SOURCES
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
   FuzzTreeConfigClient.cpp
   TreeHelpers.cpp
   main.cpp
   faulttree.cpp
   fuzztree.cpp
)
set(HEADERS
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
   FuzzTreeConfigClient.h
   TreeHelpers.h
   platform.h
   faulttree.h
   fuzztree.h
   FaultTreeTypes.h
   FuzzTreeTypes.h
)

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faulttree.xsd")
set(FUZZTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/fuzztree.xsd")

set(SCHEMAS ${FAULTTREE_XSD} ${FUZZTREE_XSD})

set(LINKED_LIBS ${XERCESC_LIBRARIES} ${BEANSTALKPP_LIB} ${Boost_LIBRARIES})
message(STATUS "${LINKED_LIBS}")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${FT_LIB_DIR}")
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS} ${SCHEMAS})
target_link_libraries(ftconfiguration ${LINKED_LIBS})

option(BUILD_TEST_EXECUTABLE OFF)#just for testing
if (BUILD_TEST_EXECUTABLE)
  add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS} ${SCHEMAS})
  target_link_libraries(ftconfiguration_exe ${LINKED_LIBS})
endif(BUILD_TEST_EXECUTABLE)

set(XSD_TO_FAULTTREE_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
  --polymorphic-type-all
  --root-element "FaultTree"
  --type-naming ucc
  --function-naming lcc
  --generate-serialization
  --namespace-map net.faulttree=faulttree
  --hxx-suffix .h
  --cxx-suffix .cpp
)

set(XSD_TO_FUZZTREE_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
  --polymorphic-type-all
  --root-element "FuzzTree"
  --type-naming ucc 
  --function-naming lcc
  --generate-serialization
  --namespace-map net.fuzztree=fuzztree 
  --hxx-suffix .h
  --cxx-suffix .cpp
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