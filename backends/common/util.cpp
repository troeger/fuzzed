#include "util.h"

#include <cstdlib>
#include <stdarg.h> 
#include <boost/lexical_cast.hpp>
#include <boost/math/special_functions/binomial.hpp>
#include <boost/range/counting_range.hpp>
#include <boost/tokenizer.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/operations.hpp>
#include <fstream>
#include <cmath>
#include <chrono>
#include <exception>
#include <algorithm>

using namespace boost;
using namespace pugi;

using std::ofstream;
using std::ifstream;

std::string util::toString(const int& i)
{
	return lexical_cast<string>(i);
}

std::string util::toString(const double& d, const int& prec /*= 5*/)
{
	std::ostringstream oss;
	oss << std::fixed << std::setprecision(prec);
	oss << d;
	return oss.str();
}

string util::toString(istream& istream)
{
	const auto pos = istream.tellg();
	const string result = string(std::istreambuf_iterator<char>(istream), std::istreambuf_iterator<char>());
	istream.seekg(pos);
	return result;
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

string util::fileNameFromPath(const string& path)
{
	return path.substr(std::min(path.find_last_of("/"), path.find_last_of("\\")) + 1);
}

int util::fileSize(const char* filename)
{
	ifstream in(filename, ifstream::in | ifstream::binary);
	in.seekg(0, ifstream::end);
	in.close();
	return (int)in.tellg(); 
}


string util::timeStamp()
{
	time_t t;
	time(&t);

	std::stringstream strm;
	strm << t;
	return strm.str();
}

double util::kOutOfN(double rate, int k, int N)
{
	if (k > N)
		return rate;
	
	double sum = 0.0L;
	for (int i : counting_range(k, N))
	{
		double binom = math::binomial_coefficient<double>(N, i);
		sum += binom * std::pow(rate, i) * std::pow(1.0 - rate, N-i);
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
		results.push_back(string(*it));
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

int util::countFiles(const string& path, const string& ext /*= ""*/)
{
	return std::count_if(
		filesystem::directory_iterator(path),
		filesystem::directory_iterator(),
		[&](filesystem::path p) { return is_regular_file(p) && p.extension() == ext; } );
}

void util::clearDirectory(const string& dir)
{
	filesystem::directory_iterator end;
	for(filesystem::directory_iterator iter(dir) ; iter != end ; ++iter)
		filesystem::remove_all(*iter);
}

bool util::beginsWith(const string& subject, const string& prefix)
{
	return subject.substr(0, prefix.length()) == prefix;
}

double util::rateFromProbability(double prob, int missionTime)
{
	// http://www.wolframalpha.com/input/?i=solve+1-e%5E%28-x+*+t%29+%3D+p+for+x+and+p%3E%3D0+and+p%3C%3D1+and+t%3E0+and+x%3E%3D0
	assert(missionTime > 0);
	
	static const double THRESHOLD = 0.00000001;
	if (1.0 - prob < THRESHOLD)
		return 1.0;

	return std::log(1.0 / (1.0 - prob)) / missionTime;
}


double util::probabilityFromRate(double rate, int missionTime)
{
	assert(missionTime > 0);
	
	static const double e = 2.71828182845904523536;
	return (1.0 - std::pow(e, -1.0 * rate * missionTime));
}

bool util::bitSet(const int var, const int pos)
{
	return !!((var) & (1<<(pos)));
}

bool util::isWritable(const string& path)
{
	FILE *fp = fopen(path.c_str(), "w");
	if (fp == nullptr)
	{
		if (errno == EACCES)
			std::cerr << "Permission denied" << std::endl;
		else
			std::cerr << "Something went wrong: " << strerror(errno) << std::endl;
		return false;
	}
	return true;
}
