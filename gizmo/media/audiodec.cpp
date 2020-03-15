#include "audiodec.h"
#include "demux.h"
#include "avout.h"
#include "general/logger.h"
#include "general/exception.h"

using namespace std;


AudioDec::AudioDec() :
	m_codecCtx(NULL),
	m_frame(NULL),
	m_output(NULL),
	m_firstPacket(true),
	m_timeBase(0.0)
{
}

AudioDec::~AudioDec()
{
}

void AudioDec::start(const AVStream *stream)
{
	AVCodec *codec = avcodec_find_decoder(stream->codecpar->codec_id);
	if (codec == NULL)
		throw EXCEPTION("can't find suitable audio codec")
			.module("AudioDec", "avcodec_find_decoder");

	logger::info("audiodec", "using codec %s (%s)", codec->name, codec->long_name);

	m_codecCtx = avcodec_alloc_context3(codec);

	if (avcodec_parameters_to_context(m_codecCtx, stream->codecpar) < 0)
		throw EXCEPTION("can't set audio codec context")
			.module("AudioDec", "avcodec_parameters_to_context");

	if (m_codecCtx->codec_type != AVMEDIA_TYPE_AUDIO)
		throw EXCEPTION("this is not audio stream")
			.module("AudioDec");

	m_timeBase = av_q2d(stream->time_base);
	m_firstPacket = true;

	int res = avcodec_open2(m_codecCtx, codec, NULL);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't open audio stream", res)
			.module("AudioDec", "avcodec_open2");

	m_frame = av_frame_alloc();

	if (m_output)
		m_output->start(stream);
}

void AudioDec::stop()
{
	if (m_output)
		m_output->stop();

	av_frame_free(&m_frame);
	avcodec_close(m_codecCtx);
	avcodec_free_context(&m_codecCtx);
}

void AudioDec::connectOutput(shared_ptr<AVOutput> output)
{
	m_output = output;
}

bool AudioDec::feed(const AVPacket *packet)
{
	int ret = avcodec_send_packet(m_codecCtx, packet);
	if (m_firstPacket)
	{
		// workaround for first packet corrupted after seek
		m_firstPacket = false;
		if (ret == AVERROR_INVALIDDATA)
		{
			logger::warn("audiodec", "first packet corrupted, ignoring");
			return false;
		}
	}

	if ((ret < 0) && (ret != AVERROR(EAGAIN)) && (ret != AVERROR_EOF))
		throw EXCEPTION_FFMPEG("audio decoder failed", ret)
			.module("AudioDec", "avcodec_send_packet")
			.time(m_timeBase * packet->pts);

	bool gotFrame = false;
	while (true)
	{
		ret = avcodec_receive_frame(m_codecCtx, m_frame);

		if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
			return gotFrame;

		if (ret < 0)
			throw EXCEPTION_FFMPEG("audio decoder failed", ret)
				.module("AudioDec", "avcodec_receive_frame")
				.time(m_timeBase * packet->pts);

		if (m_frame->channel_layout == 0)
			m_frame->channel_layout
				= av_get_default_channel_layout(m_frame->channels);

		if (m_output)
			m_output->feed(m_frame);

		gotFrame = true;
	}
}

void AudioDec::flush()
{
	AVPacket packet;
	av_init_packet(&packet);
	packet.data = NULL;
	packet.size = 0;
	while (feed(&packet));

	if (m_output)
		m_output->flush();
}

void AudioDec::discontinuity()
{
	if (m_output)
		m_output->discontinuity();
}
