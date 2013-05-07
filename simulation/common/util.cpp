#include "util.h"
#include "Constants.h"

#include <cstdlib>
#include <stdarg.h> 
#include <boost/lexical_cast.hpp>
#include <boost/math/special_functions/binomial.hpp>
#include <boost/range/counting_range.hpp>
#include <boost/tokenizer.hpp>
#include <fstream>
#include <cmath>
#include <chrono>
#include <exception>

using namespace chrono;
using namespace boost;

std::string util::toString(int i)
{
	return lexical_cast<string>(i);
}

std::string util::toString(double d, int prec /*= 5*/)
{
	std::ostringstream oss;
	oss << std::fixed << std::setprecision(prec);
	oss << d;
	return oss.str();
}

std::string util::toString(long double d, int prec /*= 5*/)
{
	std::ostringstream oss;
	oss << std::fixed << std::setprecision(prec);
	oss << d;
	return oss.str();
}

bool util::copyFile(const string& src, const string& dst)
{
	ifstream inStream(src);
	if (!inStream.good())
		throw "Input File invalid";

	ofstream outStream(dst);
	
	outStream << inStream.rdbuf();
	return outStream.good();
}

string util::fileNameFromPath(const string& path, bool withExtension)
{
	return path.substr(
		std::min(path.find_last_of("/"), path.find_last_of("\\")) + 1, 
		withExtension ? string::npos : (path.length() - path.find_last_of("."))
		);
}

int util::fileSize(const char* filename)
{
	ifstream in(filename, ifstream::in | ifstream::binary);
	in.seekg(0, ifstream::end);
	in.close();
	return (int)in.tellg(); 
}

string util::conditionString(const int placeID, ConditionType cond, const int argument)
{
	return 
		"#" + string(PLACE_IDENTIFIER) + util::toString(placeID) 
		+ conditionTypeString(cond) + util::toString(argument);
}

string util::conditionString(const string& placeIdentifier, ConditionType cond, const int argument)
{
	return 
		"#" + placeIdentifier
		+ conditionTypeString(cond) + util::toString(argument);
}

string util::timeStamp()
{
	const int time = (int)duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
	return util::toString(time);
}

long double util::kOutOfN(long double rate, int k, int N)
{
	if (k > N)
		return rate;
	
	long double sum = 0.0L;
	for (int i : counting_range(k, N))
	{
		double binom = math::binomial_coefficient<double>(N, i);
		sum += binom * std::pow(rate, i) * std::pow(1.0L - rate, N-i);
	}
	return sum;
}


struct toInt
{
	int operator()(string const &str) 
	{ 
		return atoi(str.c_str());
	}
};

void util::tokenizeIntegerString(const string& input, vector<int>& results /*out*/)
{
	char_separator<char> sep(" ,;");
	tokenizer<char_separator<char>> tok(input, sep);
	transform(tok.begin(), tok.end(), std::back_inserter(results), toInt());
}



void util::tokenizeString(const string& input, vector<string>& results /*out*/)
{
	char_separator<char> sep(" ,;");
	tokenizer<char_separator<char>> tok(input, sep);
	for (tokenizer<char_separator<char>>::iterator it = tok.begin(); it != tok.end(); ++it)
		results.emplace_back(*it);
}


void util::replaceStringInPlace(string& subject, const string& search, const std::string& replacement)
{	
	size_t pos = 0;
	while ((pos = subject.find(search, pos)) != string::npos) 
	{
		subject.replace(pos, search.length(), replacement);
		pos += replacement.length();
	}
}

void util::replaceFileExtensionInPlace(string& subject, const string& newExtension)
{
	size_t pos = subject.find_last_of(".");
	if (pos == string::npos) return;
	subject.replace(pos, subject.length()-pos, newExtension);
}

string util::nestedIDString(int n, ...)
{
	stringstream result;

	va_list args;
	va_start(args, n);

	int id = va_arg(args, int);
	result <<  id;
	for (int i = 1; i < n; ++i)
	{
		id = va_arg(args, int);
		result <<  ".";
		result << id;
	}
	va_end(args);

	return result.str();
}