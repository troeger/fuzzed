project(ftmodeltransform CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   FaultTreeNode.cpp
   
   events/Event.cpp
   events/BasicEvent.cpp
   events/TopLevelEvent.cpp
   events/UndevelopedEvent.cpp
   
   gates/StaticGate.cpp
   gates/ANDGate.cpp
   gates/ORGate.cpp
   gates/PANDGate.cpp
   gates/RedundancyGate.cpp
   gates/VotingORGate.cpp
   gates/SEQGate.cpp
   gates/FDEPGate.cpp
   gates/SpareGate.cpp
   gates/XORGate.cpp
   
   serialization/PNDocument.cpp
   serialization/PNMLDocument.cpp
   serialization/TNDocument.cpp
)

set(HEADERS
   ${HEADERS}
   FaultTreeNode.h
   FaultTreeIncludes.h
   
   events/Event.h
   events/BasicEvent.h
   events/TopLevelEvent.h
   events/UndevelopedEvent.h
   
   gates/Gate.h
   gates/StaticGate.h
   gates/DynamicGate.h
   gates/ANDGate.h
   gates/ORGate.h
   gates/PANDGate.h
   gates/VotingORGate.h
   gates/RedundancyGate.h
   gates/SEQGate.h
   gates/FDEPGate.h
   gates/SpareGate.h
   gates/XORGate.h
   
   serialization/PNDocument.h
   serialization/PNMLDocument.h
   serialization/TNDocument.h
)

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})


include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})

include_directories(${PUGIXML_INCLUDE_DIR})

if (WIN32)
   add_library(ftmodeltransform STATIC ${SOURCES} ${HEADERS})
   target_link_libraries(ftmodeltransform optimized ${PUGIXML_LIB_RELEASE})
   target_link_libraries(ftmodeltransform debug ${PUGIXML_LIB_DEBUG})
endif(WIN32)

if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
   add_library(ftmodeltransform SHARED ${SOURCES} ${HEADERS})
   set_target_properties(ftmodeltransform PROPERTIES COMPILE_FLAGS "-fPIC -rdynamic")
endif (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)

target_link_libraries(ftmodeltransform ${Boost_LIBRARIES} ftcommon)