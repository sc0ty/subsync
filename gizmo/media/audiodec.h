#ifndef __AUDIO_DECODER_H__
#define __AUDIO_DECODER_H__

#include "decoder.h"
#include "stream.h"
#include "audioout.h"

class Demux;
class AudioOutput;


class AudioDec : public Decoder
{
	public:
		AudioDec(const Demux *demux, unsigned streamId);
		AudioDec(AVStream *stream);
		virtual ~AudioDec();

		virtual void start();
		virtual void stop();

		virtual AudioFormat getFormat() const;

		void connectOutput(AudioOutput *output);

		virtual bool feed(AVPacket &packet);
		virtual void flush();
		virtual void discontinuity();

		virtual double getPosition() const;

		ConnectedAudioOutputs getConnectedOutputs() const;

	private:
		AVCodec *m_codec;
		AVCodecContext *m_codecCtx;
		AVFrame *m_frame;
		AudioOutput *m_output;
		int m_sampleSizeChs;    // sampleSize * channelsNo
		double m_timeBase;
		double m_position;
};
#endif
