#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "general/exception.h"
#include "general/logger.h"

namespace py = pybind11;

using namespace std;


void initGeneralWrapper(py::module &m)
{
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
