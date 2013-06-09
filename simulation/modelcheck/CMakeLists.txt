project(ftmodeltransform CXX)
                                                                                                                                                                                                                        
set(SOURCES
   ${SOURCE}
   main.cpp
   PNMLtoPromela.cpp
   PTNet.cpp
)

set(HEADERS
   ${HEADERS}
    PNMLtoPromela.h
	PTNet.h
)

set(LIBRARY_OUTPUT_PATH ${FT_LIB_DIR})

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${FT_INCLUDE_DIR})

include_directories(${PUGIXML_INCLUDE_DIR})

add_executable(topromela ${SOURCES} ${HEADERS})
   target_link_libraries(topromela
      ${Boost_LIBRARIES}
      ftcommon
   )