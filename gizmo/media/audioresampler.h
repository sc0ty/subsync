#ifndef __AUDIO_RESAMPLER__
#define __AUDIO_RESAMPLER__

#include "audioout.h"
#include "stream.h"
#include <cstdint>
#include <vector>
#include <memory>

extern "C"
{
#include <libswresample/swresample.h>
}


class AudioResampler : public AudioOutput
{
	public:
		AudioResampler();
		virtual ~AudioResampler();

		void connectOutput(std::shared_ptr<AudioOutput> output);

		void setParams(
				const AudioFormat &in,
				const AudioFormat &out,
				const std::vector<double> &mixMap,
				int bufferSize = 32*1024);

		virtual void start();
		virtual void stop();

		virtual void onNewData(const uint8_t *data, size_t size, double timestamp);
		virtual void onDiscontinuity();

		ConnectedAudioOutputs getConnectedOutputs() const;

	private:
		std::shared_ptr<AudioOutput> m_output;
		SwrContext *m_swr;
		uint8_t *m_buffer;
		int m_bufferSize;
		int m_inSampleSizeChs;	    // sampleSize * channelsNo
		int m_outSampleSizeChs;
};

#endif
