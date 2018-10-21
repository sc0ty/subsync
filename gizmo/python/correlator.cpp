#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "correlator.h"
#include "math/line.h"

namespace py = pybind11;


void initCorrelatorWrapper(py::module &m)
{
	/*** class Correlator ***/
	py::class_<Correlator> correlator(m, "Correlator", py::dynamic_attr());
	correlator.def(py::init<float, double, float, unsigned, float>());
	correlator.def("connectStatsCallback", &Correlator::connectStatsCallback);
	correlator.def("start", &Correlator::start);
	correlator.def("stop", &Correlator::stop);
	correlator.def("isRunning", &Correlator::isRunning);
	correlator.def("isDone", &Correlator::isDone);
	correlator.def("getProgress", &Correlator::getProgress);
	correlator.def("pushSubWord", &Correlator::pushSubWord);
	correlator.def("pushRefWord", &Correlator::pushRefWord);
	correlator.def("getSubs", &Correlator::getSubs);
	correlator.def("getRefs", &Correlator::getRefs);

	/*** struct CorrelationStats ***/
	py::class_<CorrelationStats> corrStats(m, "CorrelationStats");
	corrStats.def(py::init<>());
	corrStats.def_readonly("correlated", &CorrelationStats::correlated);
	corrStats.def_readonly("factor", &CorrelationStats::factor);
	corrStats.def_readonly("points", &CorrelationStats::points);
	corrStats.def_readonly("maxDistance", &CorrelationStats::maxDistance);
	corrStats.def_readonly("formula", &CorrelationStats::formula);
	corrStats.def("__repr__", &CorrelationStats::toString);
	corrStats.def("__str__", [](const CorrelationStats &s) {
			return s.toString("", "");
	});

	/*** class Line ***/
	py::class_<Line> line(m, "Line");
	line.def(py::init<float, float>(), py::arg("a") = 0.0f, py::arg("b") = 0.0f);
	line.def_readwrite("a", &Line::a);
	line.def_readwrite("b", &Line::b);
	line.def("getX", &Line::getX);
	line.def("getY", &Line::getY);
	line.def("__repr__", &Line::toString);
}
