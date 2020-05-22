#ifndef __SUBTITLE_DECODER_H__
#define __SUBTITLE_DECODER_H__

#include "decoder.h"
#include "text/words.h"
#include "text/ssa.h"
#include "general/notifier.h"
#include <string>
#include <functional>

extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
}


class SubtitleDec : public Decoder
{
	public:
		typedef std::function<void (
				double /* startTime */,
				double /* endTime */,
				const std::string& /* text */ )>
			SubsListener;

		typedef Notifier<double, double, const std::string&> SubsNotifier;

	public:
		SubtitleDec();
		virtual ~SubtitleDec();

		SubtitleDec(const SubtitleDec&) = delete;
		SubtitleDec(SubtitleDec&&) = delete;
		SubtitleDec& operator= (const SubtitleDec&) = delete;
		SubtitleDec& operator= (SubtitleDec&&) = delete;

		virtual void start(const AVStream *stream);
		virtual void stop();

		virtual bool feed(const AVPacket *packet);
		virtual void flush();
		virtual void discontinuity();

		void addSubsListener(SubsListener listener);
		bool removeSubsListener(SubsListener listener);

		void addWordsListener(WordsListener listener);
		bool removeWordsListener(WordsListener listener);

		void setMinWordLen(unsigned minLen);
		void setEncoding(const std::string &encoding);
		void setRightToLeft(bool rightToLeft=true);
		void setWordDelimiters(const std::string &delimiters);

	private:
		bool feedOutput(AVSubtitle &sub, double duration);
		void feedWordsOutput(float begin, float end, const char *text);

	private:
		AVCodecContext *m_codecCtx;

		SubsNotifier m_subsNotifier;
		WordsNotifier m_wordsNotifier;

		SSAParser m_ssaParser;
		unsigned m_minWordLen;

		double m_timeBase;
		double m_position;
		bool m_trimDuration;
		std::string m_encoding;
};

#endif
