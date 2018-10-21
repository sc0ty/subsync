#ifndef __STREAMINFO_H__
#define __STREAMINFO_H__

#include <string>
#include <vector>
#include <map>

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
	AudioFormat(AVSampleFormat sampleFormat, unsigned sampleRate,
			uint64_t channelLayout=0);

	unsigned getSampleSize() const;
	std::map<uint64_t, std::string> getChannelNames() const;
	std::string toString() const;
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
