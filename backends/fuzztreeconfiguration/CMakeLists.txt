set(SOURCES
   FuzzTreeTransform.cpp
   FuzzTreeConfiguration.cpp
   FuzzTreeConfigClient.cpp
   VerificationTask.cpp
   TreeHelpers.cpp
   main.cpp
)

set(HEADERS
   FuzzTreeTransform.h
   FuzzTreeConfiguration.h
   FuzzTreeConfigClient.h
   TreeHelpers.h
   VerificationTask.h
   VerificationResult.h
   platform.h
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

set(LINKED_LIBS ${XERCESC_LIBRARIES} ${Boost_LIBRARIES} ${BEANSTALKPP_LIB})
message(STATUS "${LINKED_LIBS}")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${FT_LIB_DIR}")
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS})
target_link_libraries(ftconfiguration ${COMMON_LINKED_LIBS})

option(BUILD_CONFIGURATION_EXECUTABLE OFF)#just for testing
if (BUILD_CONFIGURATION_EXECUTABLE)
  add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS})
  target_link_libraries(ftconfiguration_exe ${COMMON_LINKED_LIBS})
endif(BUILD_CONFIGURATION_EXECUTABLE)


