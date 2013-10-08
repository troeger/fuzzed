#pragma once

typedef std::string AnalysisWarning;
typedef std::string AnalysisError;

struct VerificationResult
{
public:
	void addError(const std::string& msg)	{ errors.emplace_back(msg); }
	void addWarning(const std::string& msg) { warnings.emplace_back(msg); }

	std::vector<AnalysisWarning>	warnings;
	std::vector<AnalysisError>		errors;
};
