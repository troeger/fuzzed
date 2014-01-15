#include "DeadlockMonitor.h"
#include <chrono>
#include <iostream>
#include <future>

void DeadlockMonitor::executeWithin(const int maxMillis, std::function<void()> exitRoutine)
{
	using std::chrono::steady_clock;
	using std::chrono::milliseconds;

	steady_clock::time_point const timeout =
		std::chrono::steady_clock::now() + std::chrono::milliseconds(maxMillis);

	std::future<void> fut = std::async(std::launch::async, *m_monitored);
	if (fut.wait_until(timeout) != std::future_status::ready)
	{
		std::cout << "Could not finish within " << maxMillis << " ms. Exiting.";
		exitRoutine();
	}
}

