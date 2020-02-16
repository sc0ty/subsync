#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "text/translator.h"
#include "text/dictionary.h"
#include "text/words.h"

namespace py = pybind11;

using namespace std;


void initTranslatorWrapper(py::module &m)
{
	py::class_<Dictionary, shared_ptr<Dictionary>> dictionary(m, "Dictionary");
	dictionary.def(py::init<>());
	dictionary.def("add", &Dictionary::add);
	dictionary.def("size", &Dictionary::size);
	dictionary.def("translate", &Dictionary::translate);

	py::class_<Translator, shared_ptr<Translator>> translator(m, "Translator");
	translator.def(py::init<shared_ptr<const Dictionary>>());
	translator.def("setMinWordsSim", &Translator::setMinWordsSim);
	translator.def("pushWord", &Translator::pushWord);
	translator.def("addWordsListener", &Translator::addWordsListener);
	translator.def("removeWordsListener", &Translator::removeWordsListener,
			py::arg("listener") = nullptr);

	py::class_<Word> word(m, "Word");
	word.def_readwrite("text", &Word::text);
	word.def_readwrite("time", &Word::time);
	word.def_readwrite("duration", &Word::duration);
	word.def_readwrite("score", &Word::score);
	word.def("__repr__", &Word::toString);
}
