#pragma once
#include "NumericInterval.h"
#include "Node.h"
#include <future>
#include <vector>

#include <fstream>

typedef NumericInterval AlphaCutAnalysisResult;

class AlphaCutAnalysisTask
{
public:
	AlphaCutAnalysisTask(const Node* topEvent, const unsigned int missionTime, const double alpha, std::ofstream& logfile);
	~AlphaCutAnalysisTask();

	std::future<AlphaCutAnalysisResult> run();

	const double& getAlpha() const { return m_alpha; }

protected:
	static double calculateExactlyOneOutOfN(const std::vector<interval_t>& values, unsigned int n);
	static double calculateKOutOfN(const std::vector<interval_t>& values, unsigned int k, unsigned int n);


	AlphaCutAnalysisResult analyze();
	AlphaCutAnalysisResult analyzeRecursive(const Node&);

	const unsigned int m_missionTime;
	const double m_alpha;
	const  Node* m_tree;

	std::ofstream& m_logFile;

	bool m_bDetectedUndeveloped;
};