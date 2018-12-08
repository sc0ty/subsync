#ifndef __RESAMPLER_H__
#define __RESAMPLER_H__

#include "avout.h"
#include "stream.h"
#include <cstdint>
#include <vector>
#include <memory>

extern "C"
{
#include <libswresample/swresample.h>
}


class Resampler : public AVOutput
{
	public:
		Resampler();
		virtual ~Resampler();

		void connectOutput(
				std::shared_ptr<AVOutput> output,
				const AudioFormat &format,
				int bufferSize = 32*1024);

		void setChannelMap(const std::vector<double> &mixMap);

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
		std::vector<double> m_mixMap;
		double m_timeBase;
};

#endif
