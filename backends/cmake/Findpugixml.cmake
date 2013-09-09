find_path(PUGIXML_ROOT src/pugiconfig.hpp
    $ENV{PUGIXML_ROOT}
    ${PROJECT_SOURCE_DIR}/thirdParty/pugixml
)

find_path(PUGIXML_INCLUDE_DIR pugiconfig.hpp ${PUGIXML_ROOT}/src)

find_library(PUGIXML_LIB_DEBUG
  NAMES pugixmld pugixml libpugixml
  PATHS 
	${PUGIXML_ROOT}/lib
  )

find_library(PUGIXML_LIB_RELEASE
  NAMES pugixml libpugixml
  PATHS
	${PUGIXML_ROOT}/lib
  )

set(PUGIXML_LIB
  debug ${PUGIXML_LIB_DEBUG}
  optimized ${PUGIXML_LIB_RELEASE}
  )

if (NOT PUGIXML_LIB OR NOT PUGIXML_INCLUDE_DIR)
	message(FATAL_ERROR "Could not find pugixml.")
endif()
