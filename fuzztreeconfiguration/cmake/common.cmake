MACRO( XSD_SCHEMA NAME FILE )

  #
  # Make a full path from the source directory
  #
  SET( xs_SRC "${FILE}" )

  # 
  # XSD will generate two or three C++ files (*.cxx,*.hxx). Get the
  # destination file path sans any extension and then build paths to the
  # generated files.
  #
  GET_FILENAME_COMPONENT( xs_FILE "${FILE}" NAME_WE )
  SET( xs_CXX "${CMAKE_CURRENT_BINARY_DIR}/${xs_FILE}.cxx" )
  SET( xs_HXX "${CMAKE_CURRENT_BINARY_DIR}/${xs_FILE}.hxx" )

  #
  # Add the source files to the NAME variable, which presumably will be used to
  # define the source of another target.
  #
  LIST( APPEND ${NAME} ${xs_CXX} )

  #
  # Set up a generator for the output files from the given schema file using
  # the XSD cxx-tree command.
  #
  ADD_CUSTOM_COMMAND( OUTPUT "${xs_CXX}" "${xs_HXX}"
  					COMMAND ${XSD_EXECUTABLE}
					  ARGS "cxx-tree" ${ARGN} ${CMAKE_CURRENT_SOURCE_DIR}/${xs_SRC}
					  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${xs_SRC})

  #
  # Don't fail if a generated file does not exist.
  #
  SET_SOURCE_FILES_PROPERTIES( "${xs_CXX}" "${xs_HXX}"
  							   PROPERTIES GENERATED TRUE )

ENDMACRO( XSD_SCHEMA )