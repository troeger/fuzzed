set(SOURCES
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
   FuzzTreeConfigClient.cpp
   TreeHelpers.cpp
   main.cpp
   faulttree.cpp
   fuzztree.cpp
   FaultTreeTypes.cpp
   FuzzTreeTypes.cpp
   PrintVisitor.cpp
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
   faulttree_custom.h
   fuzztree_custom.h
   Visitor.h
   PrintVisitor.h
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

set(TREE_CUSTOMIZATION_ARGS
  --custom-type Node=Visitable<Node_base>/Node_base
  --custom-type TopEvent=Visitable<TopEvent_base>/TopEvent_base
  --custom-type BasicEvent=Visitable<BasicEvent_base>/BasicEvent_base
  --custom-type HouseEvent=Visitable<HouseEvent_base>/HouseEvent_base
  --custom-type UndevelopedEvent=Visitable<UndevelopedEvent_base>/UndevelopedEvent_base
  --custom-type IntermediateEvent=Visitable<IntermediateEvent_base>/IntermediateEvent_base
  --custom-type ChildNode=Visitable<ChildNode_base>/ChildNode_base
  --custom-type Gate=Visitable<Gate_base>/Gate_base
  --custom-type And=Visitable<And_base>/And_base
  --custom-type Or=Visitable<Or_base>/Or_base
  --custom-type Xor=Visitable<Xor_base>/Xor_base
  --custom-type VotingOr=Visitable<VotingOr_base>/VotingOr_base
  --custom-type DynamicGate=Visitable<DynamicGate_base>/DynamicGate_base
  --custom-type Spare=Visitable<Spare_base>/Spare_base
  --custom-type FDEP=Visitable<FDEP_base>/FDEP_base
  --custom-type Sequence=Visitable<Sequence_base>/Sequence_base
  --custom-type PriorityAnd=Visitable<PriorityAnd_base>/PriorityAnd_base
)

set(FUZZTREE_CUSTOMIZATION_ARGS
  --custom-type RedundancyVariationPoint=Visitable<RedundancyVariationPoint_base>/RedundancyVariationPoint_base
  --custom-type FeatureVariationPoint=Visitable<FeatureVariationPoint_base>/FeatureVariationPoint_base
  --custom-type VariationPoint=Visitable<VariationPoint_base>/VariationPoint_base
  --custom-type IntermediateEventSet=Visitable<IntermediateEventSet_base>/IntermediateEventSet_base
)

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
  ${TREE_CUSTOMIZATION_ARGS}
  --hxx-prologue "#include <faulttree_custom.h>"
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
  ${TREE_CUSTOMIZATION_ARGS}
  ${FUZZTREE_CUSTOMIZATION_ARGS}
  --hxx-prologue "#include <fuzztree_custom.h>"
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