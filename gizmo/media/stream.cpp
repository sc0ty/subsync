#include "stream.h"
#include <string>
#include <sstream>

using namespace std;


static const char *channelIdToName(uint64_t id)
{
	switch (id)
	{
		case AV_CH_FRONT_LEFT:             return "front left";
		case AV_CH_FRONT_RIGHT:            return "front right";
		case AV_CH_FRONT_CENTER:           return "front center";
		case AV_CH_LOW_FREQUENCY:          return "subwoofer";
		case AV_CH_BACK_LEFT:              return "back left";
		case AV_CH_BACK_RIGHT:             return "back right";
		case AV_CH_FRONT_LEFT_OF_CENTER:   return "front left of center";
		case AV_CH_FRONT_RIGHT_OF_CENTER:  return "front right of center";
		case AV_CH_BACK_CENTER:            return "back center";
		case AV_CH_SIDE_LEFT:              return "side left";
		case AV_CH_SIDE_RIGHT:             return "side right";
		case AV_CH_TOP_CENTER:             return "top center";
		case AV_CH_TOP_FRONT_LEFT:         return "top front left";
		case AV_CH_TOP_FRONT_CENTER:       return "top front center";
		case AV_CH_TOP_FRONT_RIGHT:        return "top front right";
		case AV_CH_TOP_BACK_LEFT:          return "top back left";
		case AV_CH_TOP_BACK_CENTER:        return "top back center";
		case AV_CH_TOP_BACK_RIGHT:         return "top back right";
		case AV_CH_STEREO_LEFT:            return "stereo left";
		case AV_CH_STEREO_RIGHT:           return "stereo right";
		case AV_CH_WIDE_LEFT:              return "wide left";
		case AV_CH_WIDE_RIGHT:             return "wide right";
		case AV_CH_SURROUND_DIRECT_LEFT:   return "surround direct left";
		case AV_CH_SURROUND_DIRECT_RIGHT:  return "surround direct right";
		case AV_CH_LOW_FREQUENCY_2:        return "second subwoofer";
		default: return NULL;
	}
}

static const char *sampleFormatToName(AVSampleFormat format)
{
	switch (format)
	{
		case AV_SAMPLE_FMT_NONE: return "NONE";
		case AV_SAMPLE_FMT_U8:   return "U8";
		case AV_SAMPLE_FMT_S16:  return "S16";
		case AV_SAMPLE_FMT_S32:  return "S32";
		case AV_SAMPLE_FMT_FLT:  return "FLT";
		case AV_SAMPLE_FMT_DBL:  return "DBL";
		case AV_SAMPLE_FMT_U8P:  return "U8P";
		case AV_SAMPLE_FMT_S16P: return "S16P";
		case AV_SAMPLE_FMT_S32P: return "S32P";
		case AV_SAMPLE_FMT_FLTP: return "FLTP";
		case AV_SAMPLE_FMT_DBLP: return "DBLP";
		case AV_SAMPLE_FMT_S64:  return "S64";
		case AV_SAMPLE_FMT_S64P: return "S64P";
		default: return NULL;
	}
}


static AVCodecContext *makeCodecContext(const AVStream *stream)
{
	if (stream->codecpar == NULL)
		return NULL;

	AVCodec *codec = avcodec_find_decoder(stream->codecpar->codec_id);
	if (codec == NULL)
		return NULL;

	AVCodecContext *ctx = avcodec_alloc_context3(codec);
	if (ctx == NULL)
		return NULL;

	avcodec_parameters_to_context(ctx, stream->codecpar);
	avcodec_open2(ctx, codec, NULL);
	return ctx;
}


/*** StreamFormat ***/

StreamFormat::StreamFormat()
{}

StreamFormat::StreamFormat(unsigned no, const AVStream *stream) : no(no)
{
	if (stream == NULL)
		return;

	if (AVCodec *codec = avcodec_find_decoder(stream->codecpar->codec_id))
	{
		this->codec = codec->name ? codec->name : "";
	}

	frameRate = 0.0;
	if (!(stream->avg_frame_rate.den == 0.0))
		frameRate = (double)stream->avg_frame_rate.num / stream->avg_frame_rate.den;

	AVDictionaryEntry* lang = av_dict_get(stream->metadata, "language", NULL, 0);
	if (lang && lang->value)
		this->lang = lang->value;

	AVDictionaryEntry *title = av_dict_get(stream->metadata, "title", NULL, 0);
	if (title && title->value)
		this->title = title->value;

	if (stream->codecpar)
	{
		AVCodecContext *ctx = NULL;

		switch (stream->codecpar->codec_type)
		{
			case AVMEDIA_TYPE_VIDEO:
				this->type = "video";
				break;

			case AVMEDIA_TYPE_AUDIO:
				this->type = "audio";
				ctx = makeCodecContext(stream);
				audio = AudioFormat(ctx);
				break;

			case AVMEDIA_TYPE_SUBTITLE:
				this->type = "subtitle";
				ctx = makeCodecContext(stream);

				if (ctx && ctx->codec_descriptor)
				{
					int props = ctx->codec_descriptor->props;
					bool txt = props & AV_CODEC_PROP_TEXT_SUB;
					bool bmp = props & AV_CODEC_PROP_BITMAP_SUB;

					if (txt && !bmp) this->type += "/text";
					if (bmp && !txt) this->type += "/bitmap";
				}
				break;

			default:
				this->type = "other";
		}

		avcodec_free_context(&ctx);
	}
}

string StreamFormat::toString() const
{
	stringstream ss;
	ss << "<StreamFormat no=" << no << ", type=\"" << type << "\"";
	if (!codec.empty())  ss << ", codec=\"" << codec << "\"";
	if (!lang.empty())   ss << ", lang=\"" << lang << "\"";
	if (!title.empty())  ss << ", title=\"" << title << "\"";
	if (frameRate > 0.0) ss << ", frameRate=" << frameRate;
	if (type == "audio") ss << ", audio=" << audio.toString();
	ss << ">";
	return ss.str();
}


/*** AudioFormat ***/

AudioFormat::AudioFormat(const AVCodecContext *ctx)
{
	sampleFormat  = AV_SAMPLE_FMT_NONE;
	sampleRate    = 0;
	channelsNo    = 0;
	channelLayout = 0;

	if (ctx)
	{
		sampleFormat  = ctx->sample_fmt;
		sampleRate    = ctx->sample_rate;
		channelsNo    = ctx->channels;
		channelLayout = ctx->channel_layout;

		if (channelLayout == 0)
			channelLayout = av_get_default_channel_layout(ctx->channels);
	}
}

AudioFormat::AudioFormat(AVSampleFormat sampleFormat, unsigned sampleRate,
		uint64_t channelLayout) :
	sampleFormat(sampleFormat),
	sampleRate(sampleRate),
	channelsNo(0),
	channelLayout(channelLayout)
{
	for (uint64_t id = 1; id <= channelLayout; id <<= 1)
	{
		if (id & channelLayout)
			channelsNo++;
	}
}

unsigned AudioFormat::getSampleSize() const
{
	return av_get_bytes_per_sample(sampleFormat);
}

map<uint64_t, string> AudioFormat::getChannelNames() const
{
	map<uint64_t, string> res;
	for (uint64_t no = 1; no <= channelLayout; no <<= 1)
	{
		if (no & channelLayout)
		{
			const char *name = channelIdToName(no);
			if (name)
				res[no] = name;
		}
	}

	return res;
}

string AudioFormat::toString() const
{
	stringstream ss;
	ss << "<AudioFormat"
		<< " sampleFormat=\""   << sampleFormatToName(sampleFormat) << "\""
		<< ", sampleRate="      << sampleRate
		<< ", channelsNo="      << channelsNo
		<< ", channelLayout=0x" << std::hex << channelLayout << ">";
	return ss.str();
}

