find_path(TNETHOME TimeNET.jar
    $ENV{TNETHOME}
)

if (NOT TNETHOME)
	message(ERROR "Could not find TimeNET. Please set the environment variable TNETHOME")
endif()