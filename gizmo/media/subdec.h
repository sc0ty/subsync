#ifndef __SUBTITLE_DECODER_H__
#define __SUBTITLE_DECODER_H__

#include "decoder.h"
#include "text/words.h"
#include <string>
#include <functional>
#include <memory>

extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
}

class Demux;


class SubtitleDec : public Decoder
{
	public:
		typedef std::function<void (
				double /* startTime */,
				double /* endTime */,
				const char* /* text */ )>
			SubsCallback;

	public:
		SubtitleDec(const std::shared_ptr<Demux> demux, unsigned streamId);
		SubtitleDec(AVStream *stream);
		virtual ~SubtitleDec();

		virtual void start();
		virtual void stop();

		virtual bool feed(AVPacket &packet);
		virtual void flush();
		virtual void discontinuity();

		virtual double getPosition() const;

		void connectSubsCallback(SubsCallback callback);
		void connectWordsCallback(WordsCallback callback);

		void setMinWordLen(unsigned minLen);
		void setEncoding(const std::string &encoding);


	private:
		bool feedOutput(AVSubtitle &sub, double duration);
		void feedWordsOutput(double begin, double end, const char *text);

	private:
		AVCodec *m_codec;
		AVCodecParameters *m_codecPar;
		AVCodecContext *m_codecCtx;

		SubsCallback m_subsCb;
		WordsCallback m_wordsCb;
		unsigned m_minWordLen;

		double m_timeBase;
		double m_position;
		std::string m_encoding;
};

#endif
