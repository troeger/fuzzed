find_path(TNETDIR Simulation/scripts/simulate_edspn.py
    ${CMAKE_SOURCE_DIR}/thirdParty/TimeNET_EDSPN
    $ENV{TNETHOME}/EDSPN
)

if (NOT TNETDIR)
	message(FATAL_ERROR "Could not find TimeNET simulation files. Please set the environment variable TNETHOME")
endif()

add_definitions(-DTNETDIR="${TNETDIR}")
add_definitions(-DTNETSCRIPT="${TNETDIR}/Simulation/scripts/simulate_edspn.py")