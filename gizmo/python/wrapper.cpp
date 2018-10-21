#include <pybind11/pybind11.h>

namespace py = pybind11;


void initGeneralWrapper(py::module &);
void initExtractorWrapper(py::module &);
void initMediaWrapper(py::module &);
void initStreamWrapper(py::module &);
void initCorrelatorWrapper(py::module &);
void initTranslatorWrapper(py::module &);


PYBIND11_MODULE(gizmo, m)
{
	m.doc() = "subsync synchronization module";

	initGeneralWrapper(m);
	initExtractorWrapper(m);
	initMediaWrapper(m);
	initStreamWrapper(m);
	initCorrelatorWrapper(m);
	initTranslatorWrapper(m);
}
