#ifndef __AUDIO_DEMUX_H__
#define __AUDIO_DEMUX_H__

#include "stream.h"
#include "audioout.h"
#include <vector>
#include <memory>


class AudioDemux : public AudioOutput
{
	public:
		AudioDemux();
		virtual ~AudioDemux();

		void setOutputFormat(const AudioFormat &format);
		void setOutputFormat(unsigned sampleSize, unsigned channelsNo);
		void connectOutputChannel(unsigned channelNo,
				std::shared_ptr<AudioOutput> output);

		virtual void start();
		virtual void stop();

		virtual void onNewData(const uint8_t *data, size_t size, double timestamp);
		virtual void onDiscontinuity();

		ConnectedAudioOutputs getConnectedOutputs() const;

	private:
		unsigned m_sampleSize;
		unsigned m_channelsNo;

		std::vector<std::shared_ptr<AudioOutput>> m_outputs;
		uint8_t *m_buffer;
		size_t m_channelSize;  // size of buffer for single channel in bytes
		size_t m_pos;          // position in buffer
		double m_timestamp;    // timestamp of first packet in the buffer
};
#endif
