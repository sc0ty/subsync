#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "media/stream.h"

namespace py = pybind11;


void initStreamWrapper(py::module &m)
{
	/*** struct StreamFormat ***/
	py::class_<StreamFormat> streamFormat(m, "StreamFormat");
	streamFormat.def_readonly("no", &StreamFormat::no);
	streamFormat.def_readonly("type", &StreamFormat::type);
	streamFormat.def_readonly("codec", &StreamFormat::codec);
	streamFormat.def_readonly("lang", &StreamFormat::lang);
	streamFormat.def_readonly("title", &StreamFormat::title);
	streamFormat.def_readonly("frameRate", &StreamFormat::frameRate);
	streamFormat.def_readonly("audio", &StreamFormat::audio);
	streamFormat.def("__repr__", &StreamFormat::toString);

	/*** struct AudioFormat ***/
	py::class_<AudioFormat> audioFormat(m, "AudioFormat");
	audioFormat.def(py::init<AVSampleFormat, unsigned, uint64_t>());
	audioFormat.def_readwrite("sampleFormat", &AudioFormat::sampleFormat);
	audioFormat.def_readwrite("sampleRate", &AudioFormat::sampleRate);
	audioFormat.def_readwrite("channelsNo", &AudioFormat::channelsNo);
	audioFormat.def_readwrite("channelLayout", &AudioFormat::channelLayout);
	audioFormat.def("getSampleSize", &AudioFormat::getSampleSize);
	audioFormat.def("getChannelName", &AudioFormat::getChannelName);
	audioFormat.def("getChannelDescription", &AudioFormat::getChannelDescription);
	audioFormat.def("__repr__", &AudioFormat::toString);

	/*** enum AVSampleFormat ***/
	py::enum_<AVSampleFormat> avSampleFormat(m, "AVSampleFormat");
	avSampleFormat.value("NONE", AV_SAMPLE_FMT_NONE);
	avSampleFormat.value("U8", AV_SAMPLE_FMT_U8);
	avSampleFormat.value("S16", AV_SAMPLE_FMT_S16);
	avSampleFormat.value("S32", AV_SAMPLE_FMT_S32);
	avSampleFormat.value("FLT", AV_SAMPLE_FMT_FLT);
	avSampleFormat.value("DBL", AV_SAMPLE_FMT_DBL);
	avSampleFormat.value("U8P", AV_SAMPLE_FMT_U8P);
	avSampleFormat.value("S16P", AV_SAMPLE_FMT_S16P);
	avSampleFormat.value("S32P", AV_SAMPLE_FMT_S32P);
	avSampleFormat.value("FLTP", AV_SAMPLE_FMT_FLTP);
	avSampleFormat.value("DBLP", AV_SAMPLE_FMT_DBLP);
	avSampleFormat.value("S64", AV_SAMPLE_FMT_S64);
	avSampleFormat.value("S64P", AV_SAMPLE_FMT_S64P);
	avSampleFormat.export_values();
}
