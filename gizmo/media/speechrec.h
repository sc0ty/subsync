#ifndef __SPHINX_H__
#define __SPHINX_H__

#include "avout.h"
#include "text/words.h"
#include <pocketsphinx.h>
#include <string>


class SpeechRecognition : public AVOutput
{
	public:
		SpeechRecognition();
		virtual ~SpeechRecognition();

		SpeechRecognition(const SpeechRecognition&) = delete;
		SpeechRecognition(SpeechRecognition&&) = delete;
		SpeechRecognition& operator= (const SpeechRecognition&) = delete;
		SpeechRecognition& operator= (SpeechRecognition&&) = delete;

		virtual void start(const AVStream *stream);
		virtual void stop();

		void setParam(const std::string &key, const std::string &val);

		void addWordsListener(WordsListener listener);
		bool removeWordsListener(WordsListener listener);

		void setMinWordProb(float minProb);
		void setMinWordLen(unsigned minLen);

		virtual void feed(const AVFrame *frame);
		virtual void flush();
		virtual void discontinuity();

	private:
		void parseUtterance();

	private:
		ps_decoder_t *m_ps;
		cmd_ln_t *m_config;

		bool m_utteranceStarted;

		double m_framePeriod;
		double m_deltaTime;
		double m_timeBase;

		WordsNotifier m_wordsNotifier;
		float m_minProb;
		unsigned m_minLen;
};

#endif
