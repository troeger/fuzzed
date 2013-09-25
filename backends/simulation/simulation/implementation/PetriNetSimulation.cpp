#include "PetriNetSimulation.h"
#include "util.h"
#include "Config.h"
#include "ResultDocument.h"
#include "petrinet/PNMLImport.h"
#include "petrinet/PetriNet.h"

#include <chrono>
#include <omp.h>
#include <math.h>
#include <boost/format.hpp>
#include <boost/filesystem.hpp>
#include <thread>

using namespace chrono;
using boost::format;

bool PetriNetSimulation::run()
{	
	unsigned int numFailures = 0;
	unsigned long sumFailureTime_all = 0;
	unsigned long sumFailureTime_fail = 0;
	
	PetriNet pn = *PNMLImport::loadPNML(m_netFile.generic_string());
	if (!pn.valid()) 
		throw runtime_error("Invalid Petri Net.");

	cout <<  "----- Starting " << m_numRounds << " simulation rounds in " << omp_get_max_threads() << " threads...";

	// for checking local convergence, thread-local
	long double privateLast = 10000.0L;
	bool privateConvergence = false;
	bool privateBreak = false;

	// for checking global convergence, shared variable
	bool globalConvergence = true;
	int count = 0;

	double startTime = omp_get_wtime();

#define RELIABILITY_DISTRIBUTION	// compute the entire reliability distribution up to mission time, for statistical tests
#define OMP_PARALLELIZATION			// use OpenMP to parallelize. alternative: manual (static) work splitting over a number of C++11 threads 


#ifdef OMP_PARALLELIZATION

#ifdef RELIABILITY_DISTRIBUTION
	auto fileName = m_netFile.generic_string();
	util::replaceFileExtensionInPlace(fileName, ".statistics_timenet");
	ofstream statdoc(fileName);
	statdoc << std::endl;

	const auto maxTime = m_numSimulationSteps;
	for (int k = 0; k < maxTime; ++k)
	{
		m_numSimulationSteps = k;
#endif

#pragma omp parallel for\
	reduction(+:numFailures, sumFailureTime_all, sumFailureTime_fail, count)\
	reduction(&: globalConvergence) firstprivate(privateLast, privateConvergence, privateBreak)\
	schedule(dynamic, 1)\
	default(none) firstprivate(pn) // rely on OpenMP magical copying

	for (int i = 0; i < m_numRounds; ++i)
	{
		if (privateBreak) continue;

		pn.restoreInitialMarking();
		pn.generateRandomFiringTimes();
		SimulationRoundResult res;
		res.valid = false;
		while (!res.valid) 
			res = runOneRound(&pn);
		
		sumFailureTime_all += res.failureTime;
		++count;

		if (res.failed && res.failureTime <= m_numSimulationSteps)
		{ // the failure occurred before the end of mission time -> add up to compute R(mission time)
			++numFailures;
			sumFailureTime_fail += res.failureTime;
		}

		const long double current = (count == 0) ? 0 : ((long double)numFailures/(long double)count);
		const long double diff = std::abs(privateLast - current);

		if ((current > 0.0L) && (current < 1.0L) && (diff < m_convergenceThresh))
		{
			privateConvergence = true;
			globalConvergence &= privateConvergence;

			#pragma omp flush(globalConvergence)
			if (globalConvergence)
				privateBreak = true;
		}
		privateLast = current;
	}
// 	const double ompTime = omp_get_wtime() - startTime;
// 	startTime = omp_get_wtime();

#else

	const int threadNum = omp_get_max_threads();
	const int blockSize = std::ceil(m_numRounds / threadNum);
	std::vector<std::thread> workers(threadNum);
	std::mutex resultsMutex;

	for (int n = 0; n < threadNum; ++n)
	{
		const int startIndex = n * blockSize;
	
		workers[n] = std::thread( [&](void)
		{
			PetriNet threadLocalPN = PetriNet(pn);
			int				localCount = 0;
			unsigned long	localSumFailureTime_all = 0;
			unsigned long	localSumFailureTime_fail = 0;
			unsigned int	localNumFailures = 0;

			for (int i = startIndex; i < startIndex + blockSize; ++i)
			{
				threadLocalPN.restoreInitialMarking();
				threadLocalPN.generateRandomFiringTimes();
				
				SimulationRoundResult res;
				res.valid = false;
				while (!res.valid) 
					res = runOneRound(&threadLocalPN);

				localSumFailureTime_all += res.failureTime;
				++localCount;

				if (res.failed && res.failureTime <= m_numSimulationSteps)
				{ // the failure occurred before the end of mission time -> add up to compute R(mission time)
					++numFailures;
					localSumFailureTime_fail += res.failureTime;
				}
			}

			resultsMutex.lock();
			count				+= localCount;
			sumFailureTime_all	+= localSumFailureTime_all;
			sumFailureTime_fail += localSumFailureTime_fail;
			numFailures			+= localNumFailures;
			resultsMutex.unlock();
		});
	}

	for (int n = 0; n < threadNum; ++n)
		workers[n].join();

/*	const double cppTime = omp_get_wtime() - startTime;*/

#endif
	
	long double unreliability		= (long double)numFailures			/(long double)count;
	long double avgFailureTime_all	= (long double)sumFailureTime_all	/(long double)count;
	long double avgFailureTime_fail = (long double)sumFailureTime_fail	/(long double)numFailures;
	long double meanAvailability	= avgFailureTime_fail				/(long double)m_numSimulationSteps;
	
	SimulationResult res;
	res.reliability			= 1.0 - unreliability;
	res.meanAvailability	= meanAvailability;
	res.nFailures			= numFailures;
	res.nRounds				= count;
	res.mttf				= avgFailureTime_all;
	res.duration			= omp_get_wtime() - startTime;
	
#ifdef RELIABILITY_DISTRIBUTION
	statdoc << util::toString(res.reliability) << std::endl;
	}
#else
	printResults(res);
	writeResultXML(res);
#endif

	return true;
}

PetriNetSimulation::PetriNetSimulation(
	const boost::filesystem::path& path,
	const string& outputFileName, 
	unsigned int simulationTime,	// the maximum duration of one simulation in seconds
	unsigned int simulationSteps,	// the number of logical simulation steps performed in each round
	unsigned int numRounds,
	double convergenceThresh,
	bool simulateUntilFailure,
	unsigned int numAdaptiveRounds /*= 0*/)
	: Simulation(path, simulationTime, simulationSteps, numRounds), 
	m_outStream(nullptr),
	m_outputFileName(outputFileName),
	m_simulateUntilFailure(simulateUntilFailure),
	m_numAdaptiveRounds(numAdaptiveRounds),
	m_convergenceThresh(convergenceThresh)
{
	assert(!m_netFile.empty());
	
	if (!outputFileName.empty())
	{
		m_outStream = new ofstream(outputFileName+ ".log");
		m_debugOutStream = new ofstream(outputFileName+".debug");
	}

	cout << "Results will be written to " << outputFileName << endl;
}

// returns false, if a sequence constraint was violated
bool PetriNetSimulation::simulationStep(PetriNet* pn, int tick)
{
	tryTimedTransitions(pn, tick);
	
	// propagate all failures upwards in the correct time step
	bool immediateCanFire = true;
	while (immediateCanFire)
	{
		tryImmediateTransitions(pn, tick, immediateCanFire);
	}
	vector<TimedTransition*> toRemove;
	for (TimedTransition* tt : pn->m_inactiveTimedTransitions)
	{
		if (tt->tryUpdateStartupTime(tick))
		{
			toRemove.emplace_back(tt);
			pn->updateFiringTime(tt);
		}
	}
	for (TimedTransition* tt : toRemove)
		pn->m_inactiveTimedTransitions.erase(tt);

	return !pn->markingInvalid();
}

SimulationRoundResult PetriNetSimulation::runOneRound(PetriNet* net)
{
	static const int milli = 1000;
	
	const int maxTime = m_simulationTimeSeconds * milli;
	const auto start = high_resolution_clock::now();

	SimulationRoundResult result;
	if (net->m_activeTimedTransitions.size() == 0)
	{
		result.valid = true;
		result.failed = false;
		return result; // TODO check this earlier
	}

	auto elapsedTime = duration_cast<milliseconds>(high_resolution_clock::now()-start).count();
	try
	{
		unsigned int nextStep = net->nextFiringTime(0);
		while ((nextStep <= m_numSimulationSteps || m_simulateUntilFailure)  && elapsedTime < maxTime)
		{
			elapsedTime = duration_cast<milliseconds>(high_resolution_clock::now()-start).count();
			if (!simulationStep(net, nextStep))
			{
				result.valid = false;
				return result;
			}
			else if (net->failed())
			{
				result.failureTime = nextStep;
				result.failed = true;
				result.valid = true;
				break;
			}
			else if (nextStep == net->finalFiringTime() && !net->hasInactiveTransitions())
			{ // there are configurations where the tree can no longer fail!
				result.failureTime = m_numSimulationSteps; 
				result.failed = false;
				result.valid = true;
				break;
			}
			nextStep = net->nextFiringTime(nextStep);
		}
	}
	catch (const exception& e)
	{
		(m_outStream ? *m_outStream : cout) << "Exception during Simulation" << e.what() << endl;
		result.valid = false;
	}
	catch (...)
	{
		(m_outStream ? *m_outStream : cout) << "Unknown Exception during Simulation" << endl;
		result.valid = false;
	}

	return result;
}

PetriNetSimulation::~PetriNetSimulation()
{}

void PetriNetSimulation::tryImmediateTransitions(PetriNet* pn, int tick, bool& immediateCanFire)
{
	for (ImmediateTransition& t : pn->m_immediateTransitions)
	{
		if (t.wantsToFire(tick))
			t.tryToFire();
	}

	immediateCanFire = false;
	for (auto& p : pn->m_placeDict)
	{
		if (p.second.hasRequests())
		{
			p.second.resolveConflictsImmediate(tick);
			immediateCanFire = true;
		}
	}
}

void PetriNetSimulation::tryTimedTransitions(PetriNet* pn, int tick)
{
	for (auto& t : pn->m_activeTimedTransitions)
	{
		if (t.second->wantsToFire(tick))
			t.second->tryToFire();
	}

	for (auto& p : pn->m_placeDict)
	{
		if (p.second.hasRequests())
			p.second.resolveConflictsTimed(tick);
	}
}

void PetriNetSimulation::printResults(const SimulationResult& res)
{
	string results = str(
		format("----- File %1%, %2% simulations with %3% simulated time steps \n \
			   #Failures: %4% out of %5% \n \
			   Reliability: %6% \n \
			   Mean Availability (failing runs): %9% \n \
			   MTTF: %7% \n \
			   Simulation Duration %8% seconds") 
			   % m_netFile.generic_string()
			   % m_numRounds
			   % m_numSimulationSteps
			   % res.nFailures % res.nRounds
			   % res.reliability
			   % (m_simulateUntilFailure ? util::toString(res.mttf) : "N/A")
			   % res.duration
			   % res.meanAvailability);

	(*m_outStream) << results << endl;
	m_outStream->close();

	cout << results << endl << endl;
}


void PetriNetSimulation::writeResultXML(const SimulationResult& res)
{
	ResultDocument doc;
	doc.setResult(res);
	doc.save(m_outputFileName + ".xml");
}