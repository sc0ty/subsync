#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "text/translator.h"
#include "text/dictionary.h"

namespace py = pybind11;


void initTranslatorWrapper(py::module &m)
{
	py::class_<Dictionary> dictionary(m, "Dictionary", py::dynamic_attr());
	dictionary.def(py::init<>());
	dictionary.def("add", &Dictionary::add);
	dictionary.def("size", &Dictionary::size);
	dictionary.def("translate", &Dictionary::translate);

	py::class_<Translator> translator(m, "Translator", py::dynamic_attr());
	translator.def(py::init<const Dictionary&>());
	translator.def("setMinWordsSim", &Translator::setMinWordsSim);
	translator.def("pushWord", &Translator::pushWord);
	translator.def("connectWordsCallback",
			[] (Translator &tr, WordsCallback cb, py::handle dst) {
				(void) dst;
				tr.connectWordsCallback(cb);
			}, py::arg("callback"), py::arg("dst") = NULL);
}
