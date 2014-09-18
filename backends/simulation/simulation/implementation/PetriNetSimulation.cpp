#include "PetriNetSimulation.h"
#include "util.h"
#include "Config.h"
#include "petrinet/PNMLImport.h"
#include "petrinet/PetriNet.h"

#include <chrono>
#ifdef OMP_PARALLELIZATION
	#include <omp.h>
#endif
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

	// cout <<  "----- Starting " << m_numRounds << " simulation rounds in " << omp_get_max_threads() << " threads..." << std::endl;

	// for checking local convergence, thread-local
	double privateLast = 10000.0;
	bool privateConvergence = false;
	bool privateBreak = false;

	// for checking global convergence, shared variable
	bool globalConvergence = true;
	int count = 0;

	auto startTime = std::chrono::system_clock::now();
	RandomNumberGenerator::initGenerators();

#ifdef OMP_PARALLELIZATION
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

		unsigned int repeated = 0;
		while (!res.valid && ++repeated < m_numRounds) 
			res = runOneRound(&pn);
		
		sumFailureTime_all += res.failureTime;
		++count;

		if (res.failed && res.failureTime <= m_numSimulationSteps)
		{ // the failure occurred before the end of mission time -> add up to compute R(mission time)
			++numFailures;
			sumFailureTime_fail += res.failureTime;
		}

		const double current = (count == 0) ? 0 : ((double)numFailures/(double)count);
		const double diff = std::abs(privateLast - current);

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
#else

	const int threadNum = std::thread::hardware_concurrency();
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
				while (!res.valid && ++repeated < m_numRounds) 
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
#endif
	
	const auto elapsedTime = std::chrono::system_clock::now() - startTime;

	double unreliability		= (double)numFailures			/(double)count;
	double avgFailureTime_all	= (double)sumFailureTime_all	/(double)count;
	double avgFailureTime_fail	= (double)sumFailureTime_fail	/(double)numFailures;
	double meanAvailability		= avgFailureTime_fail			/(double)m_numSimulationSteps;
	
	SimulationResultStruct res;
	res.reliability			= 1.0 - unreliability;
	res.meanAvailability	= meanAvailability;
	res.nFailures			= numFailures;
	res.nRounds				= count;
	res.mttf				= avgFailureTime_all;
	res.duration			= (double) elapsedTime.count();
	
	// printResults(res);
	// writeResultXML(res);

	m_result = res;
	return true;
}

PetriNetSimulation::PetriNetSimulation(
	const boost::filesystem::path& inPath,
	unsigned int simulationTime,	// the maximum duration of one simulation in seconds
	unsigned int simulationSteps,	// the number of logical simulation steps performed in each round
	unsigned int numRounds,
	double convergenceThresh,
	bool simulateUntilFailure)
	: Simulation(inPath, simulationTime, simulationSteps, numRounds),
	m_simulateUntilFailure(simulateUntilFailure),
	m_convergenceThresh(convergenceThresh)
{
	assert(!m_netFile.empty());
}

// returns false, if a sequence constraint was violated
bool PetriNetSimulation::simulationStep(PetriNet* pn, int tick)
{
	tryTimedTransitions(pn, tick);
	
	// propagate all failures upwards in the correct time step
	bool immediateCanFire = true;

	unsigned int tries = 0;
	while (immediateCanFire && ++tries < m_numSimulationSteps)
	{
		tryImmediateTransitions(pn, tick, immediateCanFire);
	}
	vector<TimedTransition*> toRemove;
	for (TimedTransition* tt : pn->m_inactiveTimedTransitions)
	{
		if (tt->tryUpdateStartupTime(tick))
		{ // tt is enabled and the firing time was updated (race with enabling memory)
			toRemove.emplace_back(tt);
			pn->updateFiringTime(tt); // inserts tt's firing time in the event queue
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
		return result; // TODO check this earlier, the initial state of the petri net is invalid
	}

	auto elapsedTime = duration_cast<milliseconds>(high_resolution_clock::now()-start).count();
	try
	{
		unsigned int nextStep = net->nextFiringTime(0);
		while ((nextStep <= m_numSimulationSteps || m_simulateUntilFailure)  && elapsedTime < maxTime)
		{
			elapsedTime = duration_cast<milliseconds>(high_resolution_clock::now()-start).count();
			const bool validResult = simulationStep(net, nextStep);
			if (!validResult)
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
		std::cerr << "Exception during Simulation" << e.what() << endl;
		result.valid = false;
	}
	catch (...)
	{
		std::cerr << "Unknown Exception during Simulation" << endl;
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

void PetriNetSimulation::printResults(const SimulationResultStruct& res)
{
	const string results = str(
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

	cout << results << endl << endl;
}

void PetriNetSimulation::tidyUp()
{
	if (boost::filesystem::exists(m_netFile)) 
		boost::filesystem::remove(m_netFile);
}
