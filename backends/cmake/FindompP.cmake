find_path(OMPP_ROOT /include/pomp_lib.h
    $ENV{OMPP_ROOT}
    ${PROJECT_SOURCE_DIR}/../thirdParty/ompp-0.8.0
)

message(STATUS "ompP root: " ${OMPP_ROOT})

find_path(OMPP_INCLUDE_DIR pomp_lib.h ${OMPP_ROOT}/include/)
find_path(OMPP_BIN_DIR kinst-ompp ${OMPP_ROOT}/bin/)
find_path(OMPP_LIB_DIR libompp.a ${OMPP_ROOT}/lib/)

message(STATUS "ompP bin dir: " ${OMPP_BIN_DIR})
message(STATUS "ompP include dir: " ${OMPP_INCLUDE_DIR})
message(STATUS "ompP lib dir: " ${OMPP_LIB_DIR})


set(OMPP_CXX ${OMPP_BIN_DIR}/kinst-ompp)
set(OMPP_CC ${OMPP_BIN_DIR}/kinst-ompp)

message(STATUS "ompP compiler spec:" ${OMPP_CXX} ${OMPP_CC})