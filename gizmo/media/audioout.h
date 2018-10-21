#ifndef __AUDIO_OUTPUT_H__
#define __AUDIO_OUTPUT_H__

#include <cstddef>
#include <cstdint>
#include <tuple>
#include <vector>


class AudioOutput
{
	public:
		virtual ~AudioOutput() {};

		virtual void start() = 0;
		virtual void stop() = 0;

		virtual void onNewData(
				const uint8_t *data,
				size_t size,
				double timestamp) = 0;

		virtual void onDiscontinuity() = 0;
};


typedef std::tuple<std::string, AudioOutput*> ConnectedAudioOutput;
typedef std::vector<ConnectedAudioOutput> ConnectedAudioOutputs;

#endif
