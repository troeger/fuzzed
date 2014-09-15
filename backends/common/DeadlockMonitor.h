#pragma once

#include <cstdlib>
#include <functional>

class DeadlockMonitor
{
public:
	/**
	 * Constructor: DeadlockMonitor
	 * 
	 * Parameters: monitored - a function which might deadlock, the execution of which can be monitored and aborted after a given time.
	 */
	DeadlockMonitor(std::function<void()>* monitored) : m_monitored(monitored) {};
	
	/************************************************************************/
	/* TODO:																*/
	/*		better exitRoutine, e.g. kill thread and tidy up				*/
	/*		sadly, std::thread does not support killing. use native threads?*/
	/*		!! reason about effects on OpenMP !!							*/
	/************************************************************************/

	/**
	 * Function: executeWithin
	 * 
	 * tries to execute the provided lambda within maxMillis ms. If this does not work out, triggers the exit routine
	 * 
	 * Parameters:
	 * 		
	 * 	maxMillis - the time until the monitor aborts the execution of its monitored function.
	 *	exitRoutine - the function which is called after the monitored function is aborted.
	 */
	void executeWithin(const int maxMillis, std::function<void()> exitRoutine = []() { exit(-1); });

protected:
	/**
	 * Variable: m_monitored
	 * 
	 * the monitored function
	 */
	std::function<void()>* m_monitored;
};