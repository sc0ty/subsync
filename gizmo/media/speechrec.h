#ifndef __SPHINX_H__
#define __SPHINX_H__

#include "audioout.h"
#include "text/words.h"
#include <pocketsphinx.h>
#include <string>
#include <map>


class SpeechRecognition : public AudioOutput
{
	public:
		SpeechRecognition();
		virtual ~SpeechRecognition();

		virtual void start();
		virtual void stop();

		void setParam(const std::string &key, const std::string &val);

		void connectWordsCallback(WordsCallback callback);
		void setMinWordProb(float minProb);
		void setMinWordLen(unsigned minLen);

		virtual void onNewData(const uint8_t *data, size_t size, double timestamp);
		virtual void onDiscontinuity();

	private:
		void parseUtterance();

	private:
		ps_decoder_t *m_ps;
		cmd_ln_t *m_config;

		bool m_utteranceStarted;

		double m_framePeriod;
		double m_deltaTime;

		WordsCallback m_wordsCb;
		float m_minProb;
		unsigned m_minLen;
};

#endif
