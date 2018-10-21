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

	py::class_<Exception> error(m, "Exception");
	error.def_property_readonly("message", &Exception::message);
	error.def_property_readonly("fields", &Exception::fields);
	error.def("__repr__", &Exception::what);


	/*** logger configuration ***/
	m.def("setLoggerCallback", &setLoggerCallback);
	m.def("setDebugLevel", setDebugLevel);
}
