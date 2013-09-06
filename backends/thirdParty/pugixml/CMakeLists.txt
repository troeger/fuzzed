project(pugixml CXX)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
add_library(pugixml STATIC 
	src/pugixml.cpp
	src/pugiconfig.hpp
	src/pugixml.hpp)