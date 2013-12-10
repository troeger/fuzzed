find_path(GTEST_ROOT /include/gtest
    $ENV{GTEST_ROOT}
    ${PROJECT_SOURCE_DIR}/../gtest/gtest-1.6.0
)

find_path(GTEST_INCLUDE_DIR gtest/gtest.h ${GTEST_ROOT}/include)
find_library(GTEST_LIB gtest PATHS ${GTEST_ROOT})