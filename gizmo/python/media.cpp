#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "media/demux.h"
#include "media/subdec.h"
#include "media/audiodec.h"
#include "media/resampler.h"
#include "media/avout.h"
#include "media/speechrec.h"

namespace py = pybind11;

using namespace std;


void initMediaWrapper(py::module &m)
{
	/*** class Demux ***/
	py::class_<Demux, shared_ptr<Demux>> demux(m, "Demux");
	demux.def(py::init<const string &>());
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
	subDec.def("connectSubsCallback", &SubtitleDec::connectSubsCallback);
	subDec.def("connectWordsCallback", &SubtitleDec::connectWordsCallback);

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
	speechRec.def("connectWordsCallback",
			&SpeechRecognition::connectWordsCallback);
}
