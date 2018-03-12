#pragma once

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
#define IS_WINDOWS 1
#endif

#if IS_WINDOWS
	#define noexcept throw()
#endif

#if IS_WINDOWS

#ifdef SIMULATION_DLL
	#define FT_DLL_API __declspec(dllexport)
#else
	#define FT_DLL_API __declspec(dllimport)
#endif

#ifdef SIMULATION_STATIC
	#define FT_DLL_API 
#endif

#else
	#define FT_DLL_API
#endif /*IS_WINDOWS*/

#if IS_WINDOWS
	#define DEPRECATED __declspec(deprecated)
#else
	#define DEPRECATED __attribute__((deprecated))
#endif
