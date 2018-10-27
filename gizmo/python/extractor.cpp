#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "extractor.h"

namespace py = pybind11;


void initExtractorWrapper(py::module &m)
{
	py::class_<Extractor> extractor(m, "Extractor", py::dynamic_attr());
	extractor.def(py::init<Demux &>());
	extractor.def("getStreamsInfo", &Extractor::getStreamsInfo);
	extractor.def("selectTimeWindow", &Extractor::selectTimeWindow);
	extractor.def("connectEosCallback", &Extractor::connectEosCallback);
	extractor.def("connectErrorCallback", &Extractor::connectErrorCallback);
	extractor.def("start", &Extractor::start);
	extractor.def("stop", &Extractor::stop, py::arg("wait") = false);
	extractor.def("isRunning", &Extractor::isRunning);
}
