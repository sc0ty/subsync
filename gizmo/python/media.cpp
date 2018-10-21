#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "media/demux.h"
#include "media/subdec.h"
#include "media/audiodec.h"
#include "media/audiodmx.h"
#include "media/audioresampler.h"
#include "media/audioout.h"
#include "media/speechrec.h"

namespace py = pybind11;


void initMediaWrapper(py::module &m)
{
	/*** class Demux ***/
	py::class_<Demux> demux(m, "Demux", py::dynamic_attr());
	demux.def(py::init<const std::string &>());
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
	demux.def("getConnectedOutputs", &Demux::getConnectedOutputs);

	/*** interface Decoder ***/
	py::class_<Decoder> decoder(m, "Decoder", py::dynamic_attr());
	decoder.def("start", &Decoder::start);
	decoder.def("stop", &Decoder::stop);
	decoder.def("getPosition", &Decoder::getPosition);

	/*** class SubtitleDec ***/
	py::class_<SubtitleDec> subDec(m, "SubtitleDec", decoder, py::dynamic_attr());
	subDec.def(py::init<const Demux *, unsigned>());
	subDec.def("setMinWordLen", &SubtitleDec::setMinWordLen);
	subDec.def("setEncoding", &SubtitleDec::setEncoding);
	subDec.def("connectSubsCallback",
			[] (SubtitleDec &s, SubtitleDec::SubsCallback cb, py::handle dst) {
				(void) dst;
				s.connectSubsCallback(cb);
			}, py::arg("callback"), py::arg("dst") = NULL);
	subDec.def("connectWordsCallback",
			[] (SubtitleDec &s, WordsCallback cb, py::handle dst) {
				(void) dst;
				s.connectWordsCallback(cb);
			}, py::arg("callback"), py::arg("dst") = NULL);

	/*** class AudioDec ***/
	py::class_<AudioDec> audioDec(m, "AudioDec", decoder, py::dynamic_attr());
	audioDec.def(py::init<const Demux *, unsigned>());
	audioDec.def("getFormat", &AudioDec::getFormat);
	audioDec.def("connectOutput", &AudioDec::connectOutput);
	audioDec.def("getConnectedOutputs", &AudioDec::getConnectedOutputs);

	/*** interface AudioOutput ***/
	py::class_<AudioOutput> audioOut(m, "AudioOutput", py::dynamic_attr());

	/*** class AudioResampler ***/
	py::class_<AudioResampler> audioRes(m, "AudioResampler", audioOut,
			py::dynamic_attr());
	audioRes.def(py::init<>());
	audioRes.def("setParams", &AudioResampler::setParams,
			py::arg("input"), py::arg("output"), py::arg("mixMap"),
			py::arg("bufferSize") = 32*1024);
	audioRes.def("connectOutput", &AudioResampler::connectOutput);
	audioRes.def("getConnectedOutputs", &AudioResampler::getConnectedOutputs);

	/*** class AudioDemux ***/
	py::class_<AudioDemux> audioDemux(m, "AudioDemux", audioOut,
			py::dynamic_attr());
	audioDemux.def(py::init<>());
	audioDemux.def("setOutputFormat",
			(void (AudioDemux::*)(unsigned, unsigned))
			&AudioDemux::setOutputFormat);
	audioDemux.def("setOutputFormat",
			(void (AudioDemux::*)(const AudioFormat&))
			&AudioDemux::setOutputFormat);
	audioDemux.def("connectOutputChannel", &AudioDemux::connectOutputChannel);
	audioDemux.def("getConnectedOutputs", &AudioDemux::getConnectedOutputs);

	/*** class SpeechRecognition ***/
	py::class_<SpeechRecognition> speechRec(m, "SpeechRecognition", audioOut,
			py::dynamic_attr());
	speechRec.def(py::init<>());
	speechRec.def("setParam", &SpeechRecognition::setParam);
	speechRec.def("setMinWordProb", &SpeechRecognition::setMinWordProb);
	speechRec.def("setMinWordLen", &SpeechRecognition::setMinWordLen);
	speechRec.def("connectWordsCallback",
			[] (SpeechRecognition &sr, WordsCallback cb, py::handle dst) {
				(void) dst;
				sr.connectWordsCallback(cb);
			}, py::arg("callback"), py::arg("dst") = NULL);
}
