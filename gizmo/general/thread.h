#ifndef __THREAD_H__
#define __THREAD_H__

#if defined(__linux__)

#include <pthread.h>

void lowerThreadPriority()
{
	struct sched_param param;
	param.sched_priority = 0;
	pthread_setschedparam(pthread_self(), SCHED_BATCH, &param);
}

#elif defined(_WIN32)

#include <windows.h>

void lowerThreadPriority()
{
	SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_BELOW_NORMAL);
}

#else

#pragma message("warning: Unknown platform, thread priority control not supported")

void lowerThreadPriority()
{
}

#endif

#endif
