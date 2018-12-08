#ifndef __AV_OUTPUT_H__
#define __AV_OUTPUT_H__

#include <cstddef>
#include <cstdint>

extern "C"
{
#include <libavformat/avformat.h>
}


class AVOutput
{
	public:
		virtual ~AVOutput() {};

		virtual void start(const AVStream *stream) = 0;
		virtual void stop() = 0;

		virtual void feed(const AVFrame *frame) = 0;
		virtual void flush() = 0;
		virtual void discontinuity() = 0;
};
#endif
