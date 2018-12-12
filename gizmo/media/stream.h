#ifndef __STREAMINFO_H__
#define __STREAMINFO_H__

#include <string>
#include <vector>

extern "C"
{
#include <libavformat/avformat.h>
}


struct AudioFormat
{
	AVSampleFormat sampleFormat;
	unsigned sampleRate;
	unsigned channelsNo;
	uint64_t channelLayout;

	AudioFormat(const AVCodecContext *codecContext = NULL);
	AudioFormat(const AVFrame *frame);
	AudioFormat(AVSampleFormat sampleFormat, unsigned sampleRate,
			uint64_t channelLayout=0);

	unsigned getSampleSize() const;
	std::string getLayoutString() const;
	std::string toString() const;

	static const char *getChannelName(uint64_t id);
	static const char *getChannelDescription(uint64_t id);
	static uint64_t getChannelIdByName(const char *name);
};

struct StreamFormat
{
	unsigned no;
	std::string type;
	std::string codec;
	std::string lang;
	std::string title;
	double frameRate;

	AudioFormat audio;

	StreamFormat();
	StreamFormat(unsigned no, const AVStream *stream);
	std::string toString() const;
};

typedef std::vector<StreamFormat> StreamsFormat;

#endif
