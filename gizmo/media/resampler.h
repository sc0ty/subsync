#ifndef __RESAMPLER_H__
#define __RESAMPLER_H__

#include "avout.h"
#include "stream.h"
#include <cstdint>
#include <vector>
#include <map>
#include <tuple>
#include <memory>
#include <functional>

extern "C"
{
#include <libswresample/swresample.h>
}


class Resampler : public AVOutput
{
	public:
		typedef std::function<void (
				const AudioFormat &in,
				const AudioFormat &out)>
			FormatChangeCallback;

	public:
		Resampler();
		virtual ~Resampler();

		Resampler(const Resampler&) = delete;
		Resampler(Resampler&&) = delete;
		Resampler& operator= (const Resampler&) = delete;
		Resampler& operator= (Resampler&&) = delete;

		void connectOutput(
				std::shared_ptr<AVOutput> output,
				const AudioFormat &format,
				int bufferSize = 32*1024);

		void connectFormatChangeCallback(FormatChangeCallback callback);

		typedef std::tuple<uint64_t /* in */, uint64_t /* out */> ChannelPath;
		typedef std::map<ChannelPath, double /* gain */> ChannelsMap;
		void setChannelMap(const ChannelsMap &channelsMap);

		virtual void start(const AVStream *stream);
		virtual void stop();

		virtual void feed(const AVFrame *format);
		virtual void flush();
		virtual void discontinuity();

	private:
		void initSwrContext(const AudioFormat &out, const AudioFormat &in);

	private:
		std::shared_ptr<AVOutput> m_output;
		SwrContext *m_swr;
		AVFrame *m_outFrame;
		int m_bufferSize;
		double m_timeBase;

		ChannelsMap m_channelsMap;
		FormatChangeCallback m_formatChangeCb;
};

#endif
