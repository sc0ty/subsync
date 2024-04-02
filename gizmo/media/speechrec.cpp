#include "speechrec.h"
#include "text/utf8.h"
#include "general/exception.h"
#include <cstring>
#include <cstdint>

using namespace std;


SpeechRecognition::SpeechRecognition() :
	m_ps(NULL),
	m_config(NULL),
	m_utteranceStarted(false),
	m_framePeriod(0.0),
	m_deltaTime(-1.0),
	m_timeBase(0.0),
	m_minProb(1.0f),
	m_minLen(0)
{
	m_config = cmd_ln_parse_r(NULL, ps_args(), 0, NULL, TRUE);
	if (m_config == NULL)
		throw EXCEPTION("can't init Sphinx configuration")
			.module("SpeechRecognition", "cmd_ln_parse_r");
}

SpeechRecognition::~SpeechRecognition()
{
	ps_config_free(m_config);
}

void SpeechRecognition::setParam(const string &key, const string &val)
{
	ps_arg_t const *args = ps_args();

	for (size_t i = 0; args[i].name != NULL; i++)
	{
		if (key == args[i].name)
		{
			int type = args[i].type;
			if (type & ARG_STRING || type & ARG_INTEGER || type & ARG_FLOATING || type & ARG_BOOLEAN)
				cmd_ln_set_str_extra_r(m_config, key.c_str(), val.c_str());
			else
				throw EXCEPTION("invalid parameter type")
					.module("SpeechRecognition", "setParameter")
					.add("parameter", key)
					.add("value", val)
					.add("type", type);

			return;
		}
	}

	throw EXCEPTION("parameter not supported")
		.module("SpeechRecognition", "setParameter")
		.add("parameter", key)
		.add("value", val);
}

void SpeechRecognition::addWordsListener(WordsListener listener)
{
	m_wordsNotifier.addListener(listener);
}

bool SpeechRecognition::removeWordsListener(WordsListener listener)
{
	return m_wordsNotifier.removeListener(listener);
}

void SpeechRecognition::setMinWordProb(float minProb)
{
	m_minProb = minProb;
}

void SpeechRecognition::setMinWordLen(unsigned minLen)
{
	m_minLen = minLen;
}

void SpeechRecognition::start(const AVStream *stream)
{
	if ((m_ps = ps_init(m_config)) == NULL)
		throw EXCEPTION("can't init Sphinx engine")
			.module("SpeechRecognition", "ps_init");

	double frate = ((cmd_ln_access_r(m_config, "-frate"))->val).fl;
	m_framePeriod = 1.0 / frate;

	if (frate == 0)
		throw EXCEPTION("can't get frame rate value")
			.module("SpeechRecognition", "cmd_ln_int32_r");

	if (ps_start_utt(m_ps))
		throw EXCEPTION("can't start speech recognition")
			.module("SpeechRecognition", "ps_start_utt");

	m_utteranceStarted = false;
	m_timeBase = av_q2d(stream->time_base);
}

void SpeechRecognition::stop()
{
	if (m_ps)
	{
		if (ps_end_utt(m_ps))
			throw EXCEPTION("can't stop speech recognition")
				.module("SpeechRecognition", "ps_end_utt");

		if (m_utteranceStarted)
		{
			parseUtterance();
			m_utteranceStarted = false;
		}

		ps_free(m_ps);
		m_ps = NULL;
	}
}

void SpeechRecognition::feed(const AVFrame *frame)
{
	if (m_deltaTime < 0.0)
		m_deltaTime = m_timeBase * frame->pts;

	const int16 *data = (const int16*) frame->data[0];
	size_t size = frame->nb_samples;

	int no = ps_process_raw(m_ps, data, size, FALSE, FALSE);
	if (no < 0)
		throw EXCEPTION("speech recognition error")
			.module("SpeechRecognition", "ps_process_raw");

	uint8 inSpeech = ps_get_in_speech(m_ps);
	if (inSpeech && !m_utteranceStarted)
	{
		m_utteranceStarted = true;
	}
	if (!inSpeech && m_utteranceStarted)
	{
		if (ps_end_utt(m_ps))
			throw EXCEPTION("can't end utterance")
				.module("SpeechRecognition", "ps_end_utt");

		parseUtterance();

		if (ps_start_utt(m_ps))
			throw EXCEPTION("can't start utterance")
				.module("SpeechRecognition", "ps_start_utt");

		m_utteranceStarted = false;
	}
}

void SpeechRecognition::flush()
{
}

void SpeechRecognition::discontinuity()
{
	if (ps_end_utt(m_ps))
		throw EXCEPTION("can't stop speech recognition")
			.module("SpeechRecognition", "ps_end_utt");

	if (m_utteranceStarted)
		parseUtterance();

	m_deltaTime = -1.0;
	if (ps_start_stream(m_ps))
	{
		throw EXCEPTION("can't reset speech recognition engine")
			.module("SpeechRecognition", "sphinx", "ps_start_stream");
	}

	if (ps_start_utt(m_ps))
		throw EXCEPTION("can't start speech recognition")
			.module("SpeechRecognition", "ps_start_utt");

	m_utteranceStarted = false;
}

void SpeechRecognition::parseUtterance()
{
	for (ps_seg_t *it=ps_seg_iter(m_ps); it!=NULL; it=ps_seg_next(it))
	{
		const char *text = ps_seg_word(it);
		if (text && text[0] != '<' && text[0] != '[')
		{
			string word = text;
			if ((word.size() > 3) && (word.back() == ')'))
			{
				size_t pos = word.size() - 2;
				while (word[pos] >= '0' && word[pos] <= '9' && pos > 0)
					pos--;

				if (pos <= word.size()-3 && word[pos] == '(')
					word.resize(pos);
			}

			int begin, end;
			ps_seg_frames(it, &begin, &end);
			const double time = ((double)begin+(double)end) * m_framePeriod / 2.0;

			const int pprob = ps_seg_prob(it, NULL, NULL, NULL);
			const float prob = logmath_exp(ps_get_logmath(m_ps), pprob);

			if (Utf8::size(word) >= m_minLen && prob >= m_minProb)
				m_wordsNotifier.notify(Word(word, time + m_deltaTime, 0.0f, prob));
		}
	}
}

