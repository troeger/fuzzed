#pragma once

#define IS_WINDOWS defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
	#define noexcept throw()
#endif

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)

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
#endif

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
	#define DEPRECATED __declspec(deprecated)
#else
	#define DEPRECATED __attribute__((deprecated))
#endif