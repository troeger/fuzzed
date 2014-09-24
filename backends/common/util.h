#pragma once
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <algorithm>
#include <pugixml.hpp>
#include "platform.h"

using namespace std;

#define OUTPUT(string) (std::cout << string << std::endl)
#define CONTAINS(container, val) ( (container.find(val) != container.end()) )

#define MAX_INT std::numeric_limits<int>::max()
#define MAX_DOUBLE std::numeric_limits<double>::max()
#define MAX_LONG_DOUBLE std::numeric_limits<double>::max()
#define MAX_FLOAT std::numeric_limits<float>::max()

#define EXIT_ERROR(s) ( exit_error(s) )

inline void exit_error(std::string s)
{
	std::cerr << s << std::endl; 
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

	string toString(const int& i);
	string toString(const unsigned int& i);
	string toString(const double& d, const int& prec = 10);
	string toString(std::istream& istream);


	bool beginsWith(const string& subject, const string& prefix);

	void tokenizeIntegerString(const string& input, vector<int>& results /*out*/);
	void tokenizeString(const string& input, vector<string>& results /*out*/);
	
	void replaceStringInPlace(string& subject, const string& search, const std::string& replacement);
	void replaceFileExtensionInPlace(string& subject, const string& newExtension);

	bool bitSet(const int var, const int pos);

	std::string insideBrackets(const std::string& str);
	std::string afterComma(const std::string& str);

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

	bool isWritable(const string& path);

	/************************************************************************/
	/* Maths                                                                */
	/************************************************************************/
	double kOutOfN(double rate, int k, int N);

	double rateFromProbability(double prob, int missionTime);
	double probabilityFromRate(double rate, int missionTime);

	/************************************************************************/
	/* Code for generating n-combinations out of k, taken from:             */ 
	/* http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2008/n2639.pdf	*/
	/************************************************************************/

	// TODO use this: http://home.roadrunner.com/~hinnant/combinations.html
	namespace detail
	{
		template <class BidirectionalIterator>
		bool next_combination(
			BidirectionalIterator first1,
			BidirectionalIterator last1,
			BidirectionalIterator first2,
			BidirectionalIterator last2)
		{
			if ((first1 == last1) || (first2 == last2)) 
				return false;

			BidirectionalIterator m1 = last1;
			BidirectionalIterator m2 = last2; -- m2;
			while (--m1 != first1 && !(*m1 < *m2)) {}

			bool result = (m1 == first1) && !(*first1 < *m2);
			if (!result)
			{
				while (first2 != m2 && !(*m1 < *first2)) 
					++ first2;

				first1 = m1;
				std::iter_swap(first1, first2);
				++first1;
				++first2;
			}
			if ((first1 != last1) && (first2 != last2))
			{
				m1 = last1; m2 = first2;
				while ((m1 != first1) && (m2 != last2))
				{
					std::iter_swap(--m1, m2);
					++m2;
				}
				std::reverse(first1, m1);
				std::reverse(first1, last1);
				std::reverse(m2, last2);
				std::reverse(first2, last2);
			}
			return !result ;
		}
	}

	template <class BidirectionalIterator>
	bool next_combination(
		BidirectionalIterator first,
		BidirectionalIterator middle,
		BidirectionalIterator last)
	{
		return detail::next_combination(first, middle, middle, last);
	}
	
	template <class BidirectionalIterator>
	inline bool prev_combination(
		BidirectionalIterator first ,
		BidirectionalIterator middle ,
		BidirectionalIterator last)
	{
		return detail::next_combination(middle , last , first , middle);
	}
}