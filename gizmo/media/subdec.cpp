#include "subdec.h"
#include "demux.h"
#include "general/scope.h"
#include "general/exception.h"

using namespace std;


SubtitleDec::SubtitleDec() :
	m_codecCtx(NULL),
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
}

void SubtitleDec::stop()
{
	avcodec_close(m_codecCtx);
	avcodec_free_context(&m_codecCtx);
}

bool SubtitleDec::feed(const AVPacket *packet)
{
	if (!m_subsCb && !m_wordsCb)
		return false;

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

			if (m_subsCb)
				m_subsCb(begin, end, text);

			if (m_wordsCb)
				feedWordsOutput(begin, end, text);
		}
	}

	return gotSub;
}

void SubtitleDec::feedWordsOutput(float begin, float end, const char *data)
{
	const char *text = data;
	unsigned commas = 0;

	while (*text != '\0')
	{
		if (*text++ == ',' && ++commas >= 8)
			break;
	}

	if (commas < 8)
		text = data;

	float delta = (end - begin) / (float) strlen(text);
	const char *p = text;

	while (*p != '\0')
	{
		string word;
		size_t beg = p - text;
		size_t end = p - text;

		while (*p != '\0')
		{
			if (p[0] == '\\' && (p[1] == 'n' || p[1] == 'N'))
			{
				p += 2;
				break;
			}
			else if (p[0] == '{' && p[1] == '\\')
			{
				for (p += 2; *p != '}' && *p != '\0'; p++);
				break;
			}
			else if (strchr(" \t\n.,!?[]{}<>|\\/\"#$%-+`", *p))
			{
				p++;
				break;
			}
			else
			{
				word += *p;
			}

			p++;
			end++;
		}

		if (word.size() >= m_minWordLen)
		{
			float time = begin + delta * (float) (beg + end) / 2.0;
			m_wordsCb(Word(word, time));
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

void SubtitleDec::connectSubsCallback(SubsCallback callback)
{
	m_subsCb = callback;
}

void SubtitleDec::connectWordsCallback(WordsCallback callback)
{
	m_wordsCb = callback;
}

void SubtitleDec::setMinWordLen(unsigned minWordLen)
{
	m_minWordLen = minWordLen;
}

void SubtitleDec::setEncoding(const string &encoding)
{
	m_encoding = encoding;
}

