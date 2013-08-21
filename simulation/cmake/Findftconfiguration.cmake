find_path(FT_CONFIG_INCLUDE faulttree.h
    ${FT_CONFIG_DIR}
)

find_library(FT_CONFIG_LIB ftconfiguration PATHS 
	${FT_CONFIG_DIR}/lib
	${FT_CONFIG_DIR}
)

if (NOT FT_CONFIG_INCLUDE OR NOT FT_CONFIG_LIB)
	message(FATAL_ERROR "Could not find ftconfiguration files.")
endif()
