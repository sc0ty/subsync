#include "thread.h"
#include <string>


#if defined(USE_PYBIND11)

#include <pybind11/embed.h>
static void renamePythonThread(const std::string &name)
{
	try
	{
		pybind11::gil_scoped_acquire guard;
		pybind11::module threading = pybind11::module::import("threading");
		auto current_thread = threading.attr("current_thread")();
		current_thread.attr("setName")(name);
	}
	catch (...)
	{
	}
}

#else

#define renamePythonThread(x) (void) (x)

#endif


#if defined(__linux__)

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <pthread.h>

void lowerThreadPriority()
{
	struct sched_param param;
	param.sched_priority = 0;
	pthread_setschedparam(pthread_self(), SCHED_BATCH, &param);
}

void renameThread(const std::string &name)
{
#if __GLIBC__ >= 2 && __GLIBC_MINOR__ >= 12
	pthread_setname_np(pthread_self(), name.c_str());
#endif

	renamePythonThread(name);
}

#elif defined(_WIN32)

#include <windows.h>

void lowerThreadPriority()
{
	SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_BELOW_NORMAL);
}

void renameThread(const std::string &name)
{
	renamePythonThread(name);
}

#else

#pragma message("warning: Unknown platform, thread priority control not supported")

void lowerThreadPriority()
{
}

void renameThread(const std::string &name)
{
	renamePythonThread(name);
}

#endif
