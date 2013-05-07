#pragma once
#include <string>
#include <iostream>
#include <vector>
#include <set>
#include "Types.h"
#include "platform.h"

using namespace std;

#define OUTPUT(string) (std::cout << string << std::endl)
#define CONTAINS(container, val) ( (container.find(val) != container.end()) )

#define MAX_INT std::numeric_limits<int>::max()
#define MAX_DOUBLE std::numeric_limits<double>::max()
#define MAX_LONG_DOUBLE std::numeric_limits<long double>::max()
#define MAX_FLOAT std::numeric_limits<float>::max()

namespace util
{
	/************************************************************************/
	/* Strings                                                              */
	/************************************************************************/

#if IS_WINDOWS
	static const std::string slash="\\";
#else
	static const std::string slash="/";
#endif

	string nestedIDString(int n, ...);

	string toString(int i);
	string toString(double d, int prec = 9);
	string toString(long double d, int prec = 9);

	// returns something like #p[placeID] [cond] [argument]
	string conditionString(const int placeID, ConditionType cond, const int argument);
	string conditionString(const string& placeIdentifier, ConditionType cond, const int argument);

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

	/************************************************************************/
	/* Maths                                                                */
	/************************************************************************/
	long double kOutOfN(long double rate, int k, int N);
}