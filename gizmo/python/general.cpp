#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "general/thread.h"
#include "general/exception.h"
#include "general/logger.h"

namespace py = pybind11;

using namespace std;


void initGeneralWrapper(py::module &m)
{
	/*** class Thread ***/
	py::class_<Thread> thread(m, "Thread");
	thread.def(py::init<Thread::Runnable, const string&>(),
			py::arg("target"), py::arg("name")="");
	thread.def("isRunning", &Thread::isRunning);


	/*** class Sleeper ***/
	py::class_<Sleeper> sleeper(m, "Sleeper");
	sleeper.def(py::init<>());
	sleeper.def("sleep", &Sleeper::sleep, py::call_guard<py::gil_scoped_release>());
	sleeper.def("wake", &Sleeper::wake, py::call_guard<py::gil_scoped_release>());


	/*** class Exception ***/
	py::register_exception<Exception>(m, "Error");
	py::register_exception<ExceptionTerminated>(m, "ErrorTerminated");

	py::class_<Exception> error(m, "Exception");
	error.def_property_readonly("message", &Exception::message);
	error.def_property_readonly("fields", &Exception::fields);
	error.def("__repr__", &Exception::what);

	py::register_exception_translator([](std::exception_ptr p)
	{
		try
		{
			if (p)
				std::rethrow_exception(p);
		}
		catch (const Exception &e)
		{
			if (e.get("averror") == "AVERROR_EXIT")
				throw ExceptionTerminated(e);
			else
				std::rethrow_exception(p);
		}
	});


	/*** logger configuration ***/
	m.def("setLoggerCallback", &setLoggerCallback);
	m.def("setDebugLevel", setDebugLevel);
}
