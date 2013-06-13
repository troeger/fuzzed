#pragma once
#include <string>
#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <pugixml.hpp>
#include "Types.h"
#include "platform.h"
#include "ResultStruct.h"

using namespace std;

#define OUTPUT(string) (std::cout << string << std::endl)
#define CONTAINS(container, val) ( (container.find(val) != container.end()) )

#define MAX_INT std::numeric_limits<int>::max()
#define MAX_DOUBLE std::numeric_limits<double>::max()
#define MAX_LONG_DOUBLE std::numeric_limits<long double>::max()
#define MAX_FLOAT std::numeric_limits<float>::max()

#define EXIT_ERROR(s) ( exit_error(s) )

inline void exit_error(std::string s)
{
	std::cout << s << std::endl; 
	exit(-1);
}

namespace util
{
	/************************************************************************/
	/* Containers                                                           */
	/************************************************************************/
	template<typename T>
	void removeValue(std::vector<T> vec, T val)
	{
		vec.erase(std::remove(vec.begin(), vec.end(), val), vec.end());
	}

	/************************************************************************/
	/* Strings                                                              */
	/************************************************************************/

#if IS_WINDOWS
	static const std::string slash="\\";
#else
	static const std::string slash="/";
#endif

	string nestedIDString(int n, ...);

	string toString(const int& i);
	string toString(const double& d, const int& prec = 10);
	string toString(const long double& d, const int& prec = 10);

	// returns something like #p[placeID] [cond] [argument]
	string conditionString(const int placeID, ConditionType cond, const int argument);
	string conditionString(const string& placeIdentifier, ConditionType cond, const int argument);

	bool beginsWith(const string& subject, const string& prefix);

	void tokenizeIntegerString(const string& input, vector<int>& results /*out*/);
	void tokenizeString(const string& input, vector<string>& results /*out*/);
	
	void replaceStringInPlace(string& subject, const string& search, const std::string& replacement);
	void replaceFileExtensionInPlace(string& subject, const string& newExtension);

	/************************************************************************/
	/* Timing                                                               */
	/************************************************************************/
	string timeStamp();

	/************************************************************************/
	/* Files                                                                */
	/************************************************************************/
	int fileSize(const char* fileName);
	bool copyFile(const string& src, const string& dst);
	string fileNameFromPath(const string& path);

	int countFiles(const string& path, const string& extension = "");

	void clearDirectory(const string& dir); // remove all files from dir

	/************************************************************************/
	/* Maths                                                                */
	/************************************************************************/
	long double kOutOfN(long double rate, int k, int N);

	/************************************************************************/
	/* XML                                                                  */
	/************************************************************************/

	int		parseIntegerValue(const pugi::xml_node& node, const std::string& type, const int defaultValue);
	double	parseDoubleValue(const pugi::xml_node& node, const std::string& type, const double defaultValue);
	bool	parseBooleanValue(const pugi::xml_node& node, const std::string& type, const bool defaultValue);

	SimulationResult readResultFile(const std::string& fileName);
}