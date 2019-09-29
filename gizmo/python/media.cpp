#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "media/demux.h"
#include "media/subdec.h"
#include "media/audiodec.h"
#include "media/resampler.h"
#include "media/avout.h"
#include "media/speechrec.h"
#include "text/ngrams.h"

namespace py = pybind11;

using namespace std;


void initMediaWrapper(py::module &m)
{
	/*** class Demux ***/
	py::class_<Demux, shared_ptr<Demux>> demux(m, "Demux");
	demux.def(py::init<const string &, std::function<bool()>>(),
			py::arg("fileName"), py::arg("runCb") = nullptr);
	demux.def("getStreamsInfo", &Demux::getStreamsInfo);
	demux.def("connectDec", &Demux::connectDec);
	demux.def("disconnectDec", &Demux::disconnectDec);
	demux.def("disconnectAllDec", &Demux::disconnectAllDec);
	demux.def("getPosition", &Demux::getPosition);
	demux.def("getDuration", &Demux::getDuration);
	demux.def("start", &Demux::start);
	demux.def("stop", &Demux::stop);
	demux.def("step", &Demux::step);
	demux.def("seek", &Demux::seek);
	demux.def("notifyDiscontinuity", &Demux::notifyDiscontinuity);

	/*** interface Decoder ***/
	py::class_<Decoder, shared_ptr<Decoder>> decoder(m, "Decoder");
	decoder.def("start", &Decoder::start);
	decoder.def("stop", &Decoder::stop);

	/*** class SubtitleDec ***/
	py::class_<SubtitleDec, shared_ptr<SubtitleDec>>
		subDec(m, "SubtitleDec", decoder);
	subDec.def(py::init<>());
	subDec.def("setMinWordLen", &SubtitleDec::setMinWordLen);
	subDec.def("setEncoding", &SubtitleDec::setEncoding);
	subDec.def("setRightToLeft", &SubtitleDec::setRightToLeft);
	subDec.def("addSubsListener", &SubtitleDec::addSubsListener);
	subDec.def("removeSubsListener", &SubtitleDec::removeSubsListener,
			py::arg("listener") = nullptr);
	subDec.def("addWordsListener", &SubtitleDec::addWordsListener);
	subDec.def("removeWordsListener", &SubtitleDec::removeWordsListener,
			py::arg("listener") = nullptr);

	/*** class AudioDec ***/
	py::class_<AudioDec, shared_ptr<AudioDec>> audioDec(m, "AudioDec", decoder);
	audioDec.def(py::init<>());
	audioDec.def("connectOutput", &AudioDec::connectOutput);

	/*** interface AVOutput ***/
	py::class_<AVOutput, shared_ptr<AVOutput>> audioOut(m, "AVOutput");

	/*** class Resampler ***/
	py::class_<Resampler, shared_ptr<Resampler>>
		audioRes(m, "Resampler", audioOut);
	audioRes.def(py::init<>());
	audioRes.def("connectOutput", &Resampler::connectOutput,
			py::arg("output"), py::arg("format"),
			py::arg("bufferSize") = 32*1024);
	audioRes.def("connectFormatChangeCallback",
			&Resampler::connectFormatChangeCallback);
	audioRes.def("setChannelMap", &Resampler::setChannelMap);

	/*** class SpeechRecognition ***/
	py::class_<SpeechRecognition, shared_ptr<SpeechRecognition>>
		speechRec(m, "SpeechRecognition", audioOut);
	speechRec.def(py::init<>());
	speechRec.def("setParam", &SpeechRecognition::setParam);
	speechRec.def("setMinWordProb", &SpeechRecognition::setMinWordProb);
	speechRec.def("setMinWordLen", &SpeechRecognition::setMinWordLen);
	speechRec.def("addWordsListener", &SpeechRecognition::addWordsListener);
	speechRec.def("removeWordsListener", &SpeechRecognition::removeWordsListener,
			py::arg("listener") = nullptr);

	/*** class NgramSplitter ***/
	py::class_<NgramSplitter, shared_ptr<NgramSplitter>>
		ngramSplitter(m, "NgramSplitter");
	ngramSplitter.def(py::init<size_t>());
	ngramSplitter.def("pushWord", &NgramSplitter::pushWord);
	ngramSplitter.def("addWordsListener", &NgramSplitter::addWordsListener);
	ngramSplitter.def("removeWordsListener", &NgramSplitter::removeWordsListener,
			py::arg("listener") = nullptr);
}
