#include "subdec.h"
#include "demux.h"
#include "text/utf8.h"
#include "general/scope.h"
#include "general/logger.h"
#include "general/exception.h"

using namespace std;


static const char DEFAULT_WORD_DELIMITERS[] = " \t.,!?[]{}():<>|\\/\"#$%-+`";


SubtitleDec::SubtitleDec() :
	m_codecCtx(NULL),
	m_ssaParser(DEFAULT_WORD_DELIMITERS),
	m_minWordLen(0),
	m_timeBase(0.0),
	m_position(0.0)
{
}

SubtitleDec::~SubtitleDec()
{
}

void SubtitleDec::start(const AVStream *stream)
{
	AVCodec *codec = avcodec_find_decoder(stream->codecpar->codec_id);
	if (codec == NULL)
		throw EXCEPTION("can't find suitable subtitle decoder")
			.module("SubtitleDec", "avcodec_find_decoder");

	logger::info("subdec", "using codec %s (%s)", codec->name, codec->long_name);

	m_timeBase = av_q2d(stream->time_base);

	m_codecCtx = avcodec_alloc_context3(codec);

	if (avcodec_parameters_to_context(m_codecCtx, stream->codecpar) < 0)
		throw EXCEPTION("can't set subtitle codec context")
			.module("SubtitleDec", "avcodec_parameters_to_context");

	if (m_codecCtx->codec_type != AVMEDIA_TYPE_SUBTITLE)
		throw EXCEPTION("this is not subtitle stream")
			.module("SubtitleDec");

	AVDictionary *options = NULL;
	av_dict_set(&options, "sub_text_format", "ass", 0);

	if (!m_encoding.empty())
	{
		av_dict_set(&options, "sub_charenc_mode", "pre_decoder", 0);
		av_dict_set(&options, "sub_charenc", m_encoding.c_str(), 0);
	}

	int res = avcodec_open2(m_codecCtx, codec, &options);
	av_dict_free(&options);

	if (res < 0)
		throw EXCEPTION_FFMPEG("can't open subtitle stream", res)
			.module("SubtitleDec", "avcodec_open2");

	if (m_codecCtx->subtitle_header && m_codecCtx->subtitle_header_size)
	{
		const string header((const char *) m_codecCtx->subtitle_header,
				m_codecCtx->subtitle_header_size);
		m_subsNotifier.notify(0.0, 0.0, header.c_str());
	}
}

void SubtitleDec::stop()
{
	avcodec_close(m_codecCtx);
	avcodec_free_context(&m_codecCtx);
}

bool SubtitleDec::feed(const AVPacket *packet)
{
	AVSubtitle sub;
	int gotSub;

	int len = avcodec_decode_subtitle2(m_codecCtx, &sub, &gotSub,
			(AVPacket*) packet);

	if (len < 0)
		throw EXCEPTION_FFMPEG("subtitle decoder failed", len)
			.module("SubtitleDec", "decode", "avcodec_decode_subtitle2")
			.time((double)packet->pts * m_timeBase);

	if (!gotSub)
		return false;

	ScopeExit scopedSubFreeGuard([&sub](){ avsubtitle_free(&sub); });

	m_position = (double)packet->pts * m_timeBase;
	double duration = (double)packet->duration * m_timeBase;

	gotSub = feedOutput(sub, duration);
	return gotSub;
}

bool SubtitleDec::feedOutput(AVSubtitle &sub, double duration)
{
	bool gotSub = false;

	double begin = m_position + ((double)sub.start_display_time / 1000.0);
	double end = sub.end_display_time ?
		m_position + (double)sub.end_display_time / 1000.0 :
		begin + duration;

	for (unsigned i = 0; i < sub.num_rects; i++)
	{
		AVSubtitleRect *rect = sub.rects[i];
		const char *text = rect->type == SUBTITLE_ASS ? rect->ass : rect->text;

		if (text)
		{
			gotSub = true;
			m_subsNotifier.notify(begin, end, text);
			feedWordsOutput(begin, end, text);
		}
	}

	return gotSub;
}

void SubtitleDec::feedWordsOutput(float beginTime, float endTime, const char *data)
{
	SSAParser::WordList words;
	size_t cps = m_ssaParser.splitWords(words, data);
	cps += words.size() - 1;

	if (!words.empty())
	{
		const float ratio = (endTime - beginTime) / (float) cps;
		float time = beginTime;

		for (const string &word : words)
		{
			const size_t wordSize = Utf8::size(word);
			const float duration = ratio * (float) wordSize;

			if (wordSize >= m_minWordLen)
				m_wordsNotifier.notify(Word(word, time, duration));

			time += duration + ratio;
		}
	}
}

void SubtitleDec::flush()
{
	AVPacket packet;
	av_init_packet(&packet);
	packet.data = NULL;
	packet.size = 0;
	feed(&packet);
}

void SubtitleDec::discontinuity()
{
}

void SubtitleDec::addSubsListener(SubsListener listener)
{
	m_subsNotifier.addListener(listener);
}

bool SubtitleDec::removeSubsListener(SubsListener listener)
{
	return m_subsNotifier.removeListener(listener);
}

void SubtitleDec::addWordsListener(WordsListener listener)
{
	m_wordsNotifier.addListener(listener);
}

bool SubtitleDec::removeWordsListener(WordsListener listener)
{
	return m_wordsNotifier.removeListener(listener);
}

void SubtitleDec::setMinWordLen(unsigned minWordLen)
{
	m_minWordLen = minWordLen;
}

void SubtitleDec::setEncoding(const string &encoding)
{
	m_encoding = encoding;
}

void SubtitleDec::setRightToLeft(bool rightToLeft)
{
	m_ssaParser.setRightToLeft(rightToLeft);
}
