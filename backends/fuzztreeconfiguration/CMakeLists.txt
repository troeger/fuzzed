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

if (VARIADIC_TEMPLATES)
  set(SOURCES ${SOURCES}
    PrintVisitor.cpp
  )

  set(HEADERS ${HEADERS}
    Visitor.h
    Visitable.h
    PrintVisitor.h)
endif(VARIADIC_TEMPLATES)

set(FAULTTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/faulttree.xsd")
set(FUZZTREE_XSD "${CMAKE_CURRENT_SOURCE_DIR}/xml/fuzztree.xsd")

set(SCHEMAS ${FAULTTREE_XSD} ${FUZZTREE_XSD})

set(LINKED_LIBS ${XERCESC_LIBRARIES} ${BEANSTALKPP_LIB} ${Boost_LIBRARIES})
message(STATUS "${LINKED_LIBS}")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${FT_LIB_DIR}")
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS} ${SCHEMAS})
target_link_libraries(ftconfiguration ${LINKED_LIBS})

option(BUILD_CONFIGURATION_EXECUTABLE OFF)#just for testing
if (BUILD_CONFIGURATION_EXECUTABLE)
  add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS} ${SCHEMAS})
  target_link_libraries(ftconfiguration_exe ${LINKED_LIBS})
endif(BUILD_CONFIGURATION_EXECUTABLE)

set(XSD_TO_FAULTTREE_ARGS
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
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
  --include-with-brackets	#include with <> instead of ""
  --generate-polymorphic	#needed for xsi:type
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
  )

  add_custom_target(generateFaultTreeModel
  DEPENDS ${FAULTTREE_XSD}
  COMMAND ${XSD_EXECUTABLE}
    cxx-tree 
      ${XSD_TO_FAULTTREE_ARGS} 
      ${TREE_CUSTOMIZATION_ARGS}
      --fwd-prologue "#include <Visitable.h>"
      --output-dir ${CMAKE_CURRENT_SOURCE_DIR}
      ${FAULTTREE_XSD}
  COMMENT "Generating C++ / XML mapping files for FaultTrees"
  VERBATIM)

add_custom_target(generateFuzzTreeModel
  DEPENDS ${FUZZTREE_XSD}
  COMMAND ${XSD_EXECUTABLE} 
    cxx-tree
      ${XSD_TO_FUZZTREE_ARGS}
      ${FUZZTREE_CUSTOMIZATION_ARGS}
      --fwd-prologue "#include <Visitable.h>"
      --output-dir ${CMAKE_CURRENT_SOURCE_DIR} ${FUZZTREE_XSD}
  COMMENT "Generating C++ / XML mapping files for FuzzTrees"
  VERBATIM)

else()

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

endif(VARIADIC_TEMPLATES)



add_definitions(-DFUZZTREEXSD="${FUZZTREE_XSD}")
add_definitions(-DFAULTTREEXSD="${FAULTTREE_XSD}")