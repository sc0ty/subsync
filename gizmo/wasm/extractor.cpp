#include "media/demux.h"
#include "media/subdec.h"
#include "media/audiodec.h"
#include "media/resampler.h"
#include "media/avout.h"
#include "media/speechrec.h"
#include "media/stream.h"
#include "text/ngrams.h"
#include "text/translator.h"
#include "text/dictionary.h"
#include "text/utf8.h"
#include "general/logger.h"
#include "general/exception.h"
#include <emscripten/bind.h>
#include <emscripten/val.h>
#include <functional>
#include <cfloat>


namespace em = emscripten;
using namespace std;
using namespace std::placeholders;


template <typename T>
static void addWordsListener(shared_ptr<T> obj, em::val cb)
{
	obj->addWordsListener([cb](const Word &w)
	{
		em::val word = em::val::object();
		word.set("text", w.text);
		word.set("time", w.time);
		word.set("duration", w.duration);
		cb(word);
	});
}

template <typename T>
static void addSubsListener(shared_ptr<T> obj, em::val cb)
{
	obj->addSubsListener([cb](double startTime, double endTime, const string &text)
	{
		em::val word = em::val::object();
		word.set("start", startTime);
		word.set("end", endTime);
		word.set("text", text);
		cb(word);
	});
}

template <typename T, typename S>
static void connectWordSink(shared_ptr<T> obj, shared_ptr<S> sink)
{
	obj->addWordsListener([sink](const Word &w)
	{
		sink->pushWord(w);
	});
}

shared_ptr<Resampler> makeResampler()
{
	Resampler *resampler = new Resampler();
	auto cb = [resampler](const AudioFormat &in, const AudioFormat &out)
	{
		(void) out;

		Resampler::ChannelsMap map;
		if (in.channelLayout & AV_CH_FRONT_CENTER)
		{
			map[Resampler::ChannelPath(AV_CH_FRONT_CENTER, 1)] = 1.0;
		}
		else
		{
			for (uint64_t mask = 1; mask < in.channelLayout && mask != 0; mask <<= 1)
			{
				if (mask & in.channelLayout)
					map[Resampler::ChannelPath(mask, 1)] = 1.0f / in.channelsNo;
			}

			if (map.size() != in.channelsNo)
			{
				fprintf(stderr, "resampler: channelLayout (%zx) inconsistent with "
						"channelsNo: %zu != %u, CORRECTING\n",
						(size_t) in.channelLayout, map.size(), in.channelsNo);
				for (auto &item : map)
					item.second = 1.0f / map.size();
			}
		}
		resampler->setChannelMap(map);
	};
	resampler->connectFormatChangeCallback(cb);
	return shared_ptr<Resampler>(resampler);
}

static void resamplerConnectOutput(
		shared_ptr<Resampler> resampler,
		shared_ptr<AVOutput> output,
		AVSampleFormat sampleFormat,
		unsigned sampleRate,
		int bufferSize)
{
	const AudioFormat audioFormat(sampleFormat, sampleRate, 1);
	resampler->connectOutput(output, audioFormat, bufferSize);
}

static em::val demuxGetStreamsInfo(const shared_ptr<Demux> demux)
{
	em::val streams = em::val::array();
	for (const auto &s : demux->getStreamsInfo())
	{
		em::val stream = em::val::object();
		stream.set("no", s.no);
		stream.set("type", s.type);
		stream.set("codec", s.codec);
		stream.set("lang", s.lang);
		stream.set("title", s.title);
		if (s.frameRate)
			stream.set("frameRate", s.frameRate);
		streams.call<void>("push", stream);
	}
	return streams;
}

static em::val getCurrentException()
{
	const Exception *ex = Exception::getCurrentException();
	if (ex)
	{
		em::val res = em::val::object();
		res.set("message", ex->message());
		for (const auto field : ex->fields())
			res.set(field.first, field.second);
		return res;
	}
	return em::val::undefined();
}

static string detectCharEncoding(const string &path, size_t probeSize)
{
	char *buf = new char[probeSize + 1];
	FILE *fp = fopen(path.c_str(), "rb");
	size_t read = fread(buf, 1, probeSize, fp);
	fclose(fp);
	string res;

	if (read > 0)
	{
		buf[read] = '\0';
		if (strchr(buf, '\0') < buf + read)
			res = "binary";
		else if (Utf8::validate(buf))
			res = "UTF-8";
		else
			res = "ascii";
	}
	delete [] buf;
	return res;
}

static void setLoggerCallback(em::val cb)
{
	auto wrapper = [cb](int level, const char *module, const char *msg)
	{
		em::val log = em::val::object();
		log.set("level", level);
		log.set("module", module);
		log.set("msg", msg);
		cb(log);
	};

	logger::setLoggerCallback(wrapper);
}


EMSCRIPTEN_BINDINGS(gizmo_media)
{
	em::class_<Demux> demux("Demux");
	demux.smart_ptr_constructor<>("Demux", &make_shared<Demux, const string&>);
	demux.function("getStreamsInfo", &demuxGetStreamsInfo);
	demux.function("connectDec", &Demux::connectDec);
	demux.function("disconnectDec", &Demux::disconnectDec);
	demux.function("disconnectAllDec", &Demux::disconnectAllDec);
	demux.function("getPosition", &Demux::getPosition);
	demux.function("getDuration", &Demux::getDuration);
	demux.function("start", &Demux::start);
	demux.function("stop", &Demux::stop);
	demux.function("step", &Demux::step);
	demux.function("seek", &Demux::seek);

	em::class_<Decoder> dec("Decoder");
	dec.smart_ptr<shared_ptr<Decoder>>("Decoder");

	em::class_<SubtitleDec, em::base<Decoder>> subDec("SubtitleDec");
	subDec.smart_ptr_constructor<>("SubtitleDec", &make_shared<SubtitleDec>);
	subDec.function("setMinWordLen", &SubtitleDec::setMinWordLen);
	subDec.function("setEncoding", &SubtitleDec::setEncoding);
	subDec.function("setRightToLeft", &SubtitleDec::setRightToLeft);
	subDec.function("addSubsListener", &addSubsListener<SubtitleDec>);
	subDec.function("addWordsListener", &addWordsListener<SubtitleDec>);
	subDec.function("connectTranslator", &connectWordSink<SubtitleDec, Translator>);
	subDec.function("connectNgramSplitter", &connectWordSink<SubtitleDec, NgramSplitter>);

	em::class_<AudioDec, em::base<Decoder>> audioDec("AudioDec");
	audioDec.smart_ptr_constructor<>("AudioDec", &make_shared<AudioDec>);
	audioDec.function("connectOutput", &AudioDec::connectOutput);

	em::class_<AVOutput> avOutput("AVOutput");
	avOutput.smart_ptr<shared_ptr<AVOutput>>("AVOutput");

	em::class_<Resampler, em::base<AVOutput>> audioRes("Resampler");
	audioRes.smart_ptr_constructor<>("Resampler", &makeResampler);
	audioRes.function("connectOutput", &resamplerConnectOutput);
	audioRes.function("connectFormatChangeCallback", &Resampler::connectFormatChangeCallback);
	audioRes.function("setChannelMap", &Resampler::setChannelMap);

	em::class_<SpeechRecognition, em::base<AVOutput>> speechRec("SpeechRecognition");
	speechRec.smart_ptr_constructor<>("SpeechRecognition", &make_shared<SpeechRecognition>);
	speechRec.function("setParam", &SpeechRecognition::setParam);
	speechRec.function("setMinWordProb", &SpeechRecognition::setMinWordProb);
	speechRec.function("setMinWordLen", &SpeechRecognition::setMinWordLen);
	speechRec.function("addWordsListener", &addWordsListener<SpeechRecognition>);
	speechRec.function("connectTranslator", &connectWordSink<SpeechRecognition, Translator>);
	speechRec.function("connectNgramSplitter", &connectWordSink<SpeechRecognition, NgramSplitter>);

	em::class_<NgramSplitter> ngramSplitter("NgramSplitter");
	ngramSplitter.smart_ptr_constructor<>("NgramSplitter", &make_shared<NgramSplitter, size_t>);
	ngramSplitter.function("pushWord", &NgramSplitter::pushWord);
	ngramSplitter.function("addWordsListener", &addWordsListener<NgramSplitter>);
	ngramSplitter.function("connectTranslator", &connectWordSink<NgramSplitter, Translator>);

	em::class_<Dictionary> dictionary("Dictionary");
	dictionary.smart_ptr_constructor<>("Dictionary", &make_shared<Dictionary>);
	dictionary.function("add", &Dictionary::add);
	dictionary.function("size", &Dictionary::size);
	dictionary.function("translate", &Dictionary::translate);

	em::class_<Translator> translator("Translator");
	translator.smart_ptr_constructor<>("Translator", &make_shared<Translator, shared_ptr<Dictionary>>);
	translator.function("setMinWordsSim", &Translator::setMinWordsSim);
	translator.function("pushWord", &Translator::pushWord);
	translator.function("addWordsListener", &addWordsListener<Translator>);

	em::enum_<AVSampleFormat> avSampleFormat("AVSampleFormat");
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

	em::register_vector<StreamFormat>("StreamsFormat");

	em::function("detectCharEncoding", &detectCharEncoding);
	em::function("setDebugLevel", &logger::setDebugLevel);
	em::function("setLoggerCallback", &setLoggerCallback);
	em::function("getCurrentException", &getCurrentException);
}
