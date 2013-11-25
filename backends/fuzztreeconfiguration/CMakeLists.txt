project(fuzztreeconfiguration)

set(SOURCES
  FuzzTreeTransform.cpp
  FuzzTreeConfiguration.cpp
  VerificationTask.cpp
  TreeHelpers.cpp
  main.cpp
)

set(HEADERS
  FuzzTreeTransform.h
  FuzzTreeConfiguration.h
  TreeHelpers.h
  VerificationTask.h
  VerificationResult.h
  platform.h
)

if (VARIADIC_TEMPLATES)
  set(SOURCES ${SOURCES}
    PrintVisitor.cpp)

  set(HEADERS ${HEADERS}
    Visitor.h
    Visitable.h
    PrintVisitor.h)
endif(VARIADIC_TEMPLATES)

# Compile as library for usage from analysis executable
add_library(ftconfiguration STATIC ${SOURCES} ${HEADERS})
target_link_libraries(ftconfiguration common_model)

# compile as executable for explicit configuration determination
add_executable(ftconfiguration_exe ${SOURCES} ${HEADERS})
target_link_libraries(ftconfiguration_exe common_model)
