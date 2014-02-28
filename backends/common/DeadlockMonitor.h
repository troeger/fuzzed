#pragma once

#include <cstdlib>
#include <functional>

class DeadlockMonitor
{
public:
	DeadlockMonitor(std::function<void()>* monitored) : m_monitored(monitored) {};
	
	/************************************************************************/
	/* tries to execute the provided lambda within maxMillis ms.			*/
	/* if this does not work out, triggers the exit routine					*/
	/* TODO:																*/
	/*		better exitRoutine, e.g. kill thread and tidy up				*/
	/*		sadly, std::thread does not support killing. use native threads?*/
	/*		!! reason about effects on OpenMP !!							*/
	/************************************************************************/

	void executeWithin(const int maxMillis, std::function<void()> exitRoutine = []() { exit(-1); });

protected:
	std::function<void()>* m_monitored;
};