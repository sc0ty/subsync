#include "thread.h"
#include <pybind11/embed.h>
#include <memory>
#include <string>

namespace py = pybind11;


static void renamePythonThread(const std::string &name)
{
	try
	{
		py::gil_scoped_acquire guard;
		py::module threading = py::module::import("threading");
		auto current_thread = threading.attr("current_thread")();
		current_thread.attr("setName")(name);
	}
	catch (...)
	{
	}
}


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
