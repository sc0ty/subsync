#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <vector>
#include <tuple>

#include "correlator.h"
#include "math/line.h"

namespace py = pybind11;


typedef std::vector<std::tuple<float, float>> PointsList;
static PointsList convertPointsList(const Points &pts);


void initCorrelatorWrapper(py::module &m)
{
	/*** class Correlator ***/
	py::class_<Correlator> correlator(m, "Correlator");
	correlator.def(py::init<float, double, float, unsigned, float>(),
			py::arg("windowSize"), py::arg("minCorrelation"),
			py::arg("maxDist"), py::arg("minPointsNo"), py::arg("minWordsSim"));
	correlator.def("connectStatsCallback", &Correlator::connectStatsCallback);
	correlator.def("start", &Correlator::start, py::arg("threadName") = "");
	correlator.def("stop", &Correlator::stop, py::arg("force") = false);
	correlator.def("wait", &Correlator::wait);
	correlator.def("isRunning", &Correlator::isRunning);
	correlator.def("getProgress", &Correlator::getProgress);
	correlator.def("pushSubWord", &Correlator::pushSubWord);
	correlator.def("pushRefWord", &Correlator::pushRefWord);
	correlator.def("pushSubtitle", &Correlator::pushSubtitle);
	correlator.def("getSubs", &Correlator::getSubs);
	correlator.def("getRefs", &Correlator::getRefs);
	correlator.def("getAllPoints", [](const Correlator &c) {
			return convertPointsList(c.getAllPoints());
	});
	correlator.def("getUsedPoints", [](const Correlator &c) {
			return convertPointsList(c.getUsedPoints());
	});

	/*** struct CorrelationStats ***/
	py::class_<CorrelationStats> corrStats(m, "CorrelationStats");
	corrStats.def(py::init<>());
	corrStats.def_readonly("correlated", &CorrelationStats::correlated);
	corrStats.def_readonly("factor", &CorrelationStats::factor);
	corrStats.def_readonly("points", &CorrelationStats::points);
	corrStats.def_readonly("maxDistance", &CorrelationStats::maxDistance);
	corrStats.def_readonly("formula", &CorrelationStats::formula);
	corrStats.def_readonly("coverage", &CorrelationStats::coverage);
	corrStats.def("__repr__", &CorrelationStats::toString);
	corrStats.def("__str__", &CorrelationStats::toString);

	/*** class Line ***/
	py::class_<Line> line(m, "Line");
	line.def(py::init<float, float>(), py::arg("a") = 0.0f, py::arg("b") = 0.0f);
	line.def_readwrite("a", &Line::a);
	line.def_readwrite("b", &Line::b);
	line.def("getX", &Line::getX);
	line.def("getY", &Line::getY);
	line.def("__repr__", &Line::toString);
}


PointsList convertPointsList(const Points &pts)
{
	PointsList res;
	for (const Point &p: pts)
		res.push_back(std::make_tuple(p.x, p.y));
	return res;
}
