#ifndef __DECODER_H__
#define __DECODER_H__

#include <cstddef>
#include <cstdint>

extern "C"
{
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
}


class Decoder
{
	public:
		virtual ~Decoder() {};

		virtual void start() = 0;
		virtual void stop() = 0;

		virtual bool feed(AVPacket &packet) = 0;
		virtual void flush() = 0;
		virtual void discontinuity() = 0;

		virtual double getPosition() const = 0;
};

#endif
