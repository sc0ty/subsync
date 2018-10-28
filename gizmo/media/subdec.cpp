#include "subdec.h"
#include "demux.h"
#include "general/exception.h"

using namespace std;


SubtitleDec::SubtitleDec(const shared_ptr<Demux> demux, unsigned streamId)
	: SubtitleDec(demux->getStreamRawData(streamId))
{
}

SubtitleDec::SubtitleDec(AVStream *stream) :
	m_codec(NULL),
	m_codecPar(stream->codecpar),
	m_codecCtx(NULL),
	m_minWordLen(0),
	m_timeBase(0.0),
	m_position(0.0)
{
	m_codec = avcodec_find_decoder(stream->codecpar->codec_id);
	if (m_codec == NULL)
		throw EXCEPTION("can't find suitable audio codec")
			.module("SubtitleDec", "avcodec_find_decoder");

	m_timeBase = (double)stream->time_base.num/(double)stream->time_base.den;
}

SubtitleDec::~SubtitleDec()
{
}

void SubtitleDec::start()
{
	m_codecCtx = avcodec_alloc_context3(m_codec);

	m_codec = avcodec_find_decoder(m_codecPar->codec_id);
	if (m_codec == NULL)
		throw EXCEPTION("can't find suitable subtitle decoder")
			.module("SubtitleDec", "avcodec_find_decoder");

	if (avcodec_parameters_to_context(m_codecCtx, m_codecPar) < 0)
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

	int res = avcodec_open2(m_codecCtx, m_codec, &options);
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

bool SubtitleDec::feed(AVPacket &packet)
{
	if (!m_subsCb && !m_wordsCb)
		return false;

	AVSubtitle sub;
	int gotSub;

	int len = avcodec_decode_subtitle2(m_codecCtx, &sub, &gotSub, &packet);
	if (len < 0)
		throw EXCEPTION_FFMPEG("subtitle decoder failed", len)
			.module("SubtitleDec", "decode", "avcodec_decode_subtitle2")
			.time((double)packet.pts * m_timeBase);

	if (!gotSub)
		return false;

	unique_ptr<AVSubtitle, void(*)(AVSubtitle*)>
		scopedSubFreeGuard(&sub, &avsubtitle_free);

	m_position = (double)packet.pts * m_timeBase;
	double duration = (double)packet.duration * m_timeBase;

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

void SubtitleDec::feedWordsOutput(double begin, double end, const char *data)
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

	double delta = (end - begin) / (double) strlen(text);
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
			double time = begin + delta * (double) (beg + end) / 2.0;
			m_wordsCb(word, time);
		}
	}
}

void SubtitleDec::flush()
{
	AVPacket packet;
	av_init_packet(&packet);
	packet.data = NULL;
	packet.size = 0;
	feed(packet);
}

void SubtitleDec::discontinuity()
{
}

double SubtitleDec::getPosition() const
{
	return m_position;
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

