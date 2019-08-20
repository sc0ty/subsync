#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "text/translator.h"
#include "text/dictionary.h"
#include "text/words.h"

namespace py = pybind11;


void initTranslatorWrapper(py::module &m)
{
	py::class_<Dictionary> dictionary(m, "Dictionary");
	dictionary.def(py::init<size_t, bool, bool, size_t, size_t>(),
			py::arg("minLen"),
			py::arg("rightToLeftKey") = false,
			py::arg("rightToLeftVal") = false,
			py::arg("ngramsKey") = 0,
			py::arg("ngramsVal") = 0);

	dictionary.def("add", &Dictionary::add);
	dictionary.def("size", &Dictionary::size);
	dictionary.def("translate", &Dictionary::translate);

	py::class_<Translator> translator(m, "Translator");
	translator.def(py::init<const Dictionary&>());
	translator.def("setMinWordsSim", &Translator::setMinWordsSim);
	translator.def("pushWord", &Translator::pushWord);
	translator.def("connectWordsCallback", &Translator::connectWordsCallback);

	py::class_<Word> word(m, "Word");
	word.def_readwrite("text", &Word::text);
	word.def_readwrite("time", &Word::time);
	word.def_readwrite("score", &Word::score);
}
