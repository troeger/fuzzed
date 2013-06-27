find_path(PUGIXML_ROOT src/pugiconfig.hpp
    $ENV{PUGIXML_ROOT}
    ${PROJECT_SOURCE_DIR}/thirdParty/pugixml
)

find_path(PUGIXML_INCLUDE_DIR pugiconfig.hpp ${PUGIXML_ROOT}/src)

if(WIN32)
	find_library(PUGIXML_LIB_RELEASE pugixml PATHS ${PUGIXML_ROOT}/lib)
	find_library(PUGIXML_LIB_DEBUG pugixmld PATHS ${PUGIXML_ROOT}/lib)
	message("Using Pugixml as a lib")
endif(WIN32)