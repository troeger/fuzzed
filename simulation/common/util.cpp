#include "util.h"
#include "Constants.h"

#include <cstdlib>
#include <stdarg.h> 
#include <boost/lexical_cast.hpp>
#include <boost/math/special_functions/binomial.hpp>
#include <boost/tokenizer.hpp>
#include <boost/filesystem/path.hpp>

#include <fstream>
#include <cmath>
#include <chrono>
#include <exception>
#include <algorithm>

using namespace chrono;
using namespace boost;
using namespace pugi;

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

std::string util::toString(const long double& d, const int& prec /*= 5*/)
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
	for (int i = k; i<N; ++i)
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

int util::countFiles(const string& path, const string& ext /*= ""*/)
{
	assert(false && "this had to be removed because of boost issues");
	return 0;
	//return std::count_if(
	//	filesystem::directory_iterator(path),
	//	filesystem::directory_iterator(),
	//	[&](filesystem::path p) { return is_regular_file(p) && p.extension() == ext; } );
}

void util::clearDirectory(const string& dir)
{
	//filesystem::directory_iterator end;
	//for(filesystem::directory_iterator iter(dir) ; iter != end ; ++iter)
	//	filesystem::remove_all(*iter);
}

bool util::beginsWith(const string& subject, const string& prefix)
{
	return subject.substr(0, prefix.length()) == prefix;
}


bool util::parseBooleanValue(const xml_node& node, const string& type, const bool defaultValue)
{
	const xml_node valNode = node.child(type.c_str());
	if (valNode.empty())
		return defaultValue;

	const xml_node child = valNode.child("value");
	if (child.empty())
		throw runtime_error("Value node not found");

	return child.text().as_bool(defaultValue);
}

double util::parseDoubleValue(const xml_node& node, const string& type, const double defaultValue)
{
	const xml_node valNode = node.child(type.c_str());
	if (valNode.empty())
		return defaultValue;

	const xml_node child = valNode.child("value");
	if (child.empty())
		throw runtime_error("Value node not found");

	return child.text().as_double(defaultValue);
}

int util::parseIntegerValue(const xml_node& node, const string& type, const int defaultValue)
{
	xml_node valNode = node.child(type.c_str());
	if (!valNode)
		return defaultValue;

	xml_node child = valNode.child("value");
	if (!child)
		throw runtime_error("Value node not found");

	return child.text().as_int(defaultValue);
}

SimulationResult util::readResultFile(const std::string& fileName)
{
	using namespace simulation;
	
	SimulationResult res;
	pugi::xml_document resultDoc;
	if (!resultDoc.load_file(fileName.c_str()))
		return res;
	pugi::xml_node topNode = resultDoc.child(SIMULATION_RESULT);
	if (topNode.empty())
		return res;

	res.reliability			= topNode.attribute(RELIABILITY).as_double(-1.0);
	res.meanAvailability	= topNode.attribute(AVAILABILTIY).as_double(-1.0);
	res.mttf				= topNode.attribute(MTTF).as_double(-1.0);
	res.nRounds				= topNode.attribute(NROUNDS).as_uint(0);
	res.nFailures			= topNode.attribute(NFAILURES).as_uint(0);

	return res;
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
