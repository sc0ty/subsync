#include "audiodec.h"
#include "demux.h"
#include "audioout.h"
#include "general/exception.h"

using namespace std;


AudioDec::AudioDec(const shared_ptr<Demux> demux, unsigned streamId)
	: AudioDec(demux->getStreamRawData(streamId))
{
}

AudioDec::AudioDec(AVStream *stream) :
	m_codec(NULL),
	m_codecCtx(NULL),
	m_frame(NULL),
	m_output(NULL),
	m_sampleSizeChs(0),
	m_timeBase(0.0),
	m_position(0.0)
{
	m_codec = avcodec_find_decoder(stream->codecpar->codec_id);
	if (m_codec == NULL)
		throw EXCEPTION("can't find suitable audio codec")
			.module("AudioDec", "avcodec_find_decoder");

	m_codecCtx = avcodec_alloc_context3(m_codec);

	if (avcodec_parameters_to_context(m_codecCtx, stream->codecpar) < 0)
		throw EXCEPTION("can't set audio codec context")
			.module("AudioDec", "avcodec_parameters_to_context");

	if (m_codecCtx->codec_type != AVMEDIA_TYPE_AUDIO)
		throw EXCEPTION("this is not audio stream")
			.module("AudioDec");

	AVCodecParameters *cp = stream->codecpar;
	int bytesPerSample = av_get_bytes_per_sample((AVSampleFormat) cp->format);
	m_sampleSizeChs = bytesPerSample * cp->channels;

	m_timeBase = (double)stream->time_base.num/(double)stream->time_base.den;
}

AudioDec::~AudioDec()
{
	avcodec_free_context(&m_codecCtx);
}

void AudioDec::start()
{
	int res = avcodec_open2(m_codecCtx, m_codec, NULL);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't open audio stream", res)
			.module("AudioDec", "avcodec_open2");

	m_frame = av_frame_alloc();

	if (m_output)
		m_output->start();
}

void AudioDec::stop()
{
	if (m_output)
		m_output->stop();

	av_frame_free(&m_frame);
	avcodec_close(m_codecCtx);
}

void AudioDec::connectOutput(shared_ptr<AudioOutput> output)
{
	m_output = output;
}

AudioFormat AudioDec::getFormat() const
{
	return AudioFormat(m_codecCtx);
}

bool AudioDec::feed(AVPacket &packet)
{
	int ret = avcodec_send_packet(m_codecCtx, &packet);
	if ((ret < 0) && (ret != AVERROR(EAGAIN)) && (ret != AVERROR_EOF))
		throw EXCEPTION_FFMPEG("audio decoder failed", ret)
			.module("AudioDec", "avcodec_send_packet")
			.time((double)packet.pts * m_timeBase);

	bool gotFrame = false;
	while (true)
	{
		ret = avcodec_receive_frame(m_codecCtx, m_frame);

		if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
			return gotFrame;

		if (ret < 0)
			throw EXCEPTION_FFMPEG("audio decoder failed", ret)
				.module("AudioDec", "avcodec_receive_frame")
				.time((double)packet.pts * m_timeBase);

		m_position = (double)packet.pts * m_timeBase;

		if (m_output)
		{
			m_output->onNewData(
					(const uint8_t*) m_frame->extended_data,
					m_frame->nb_samples * m_sampleSizeChs,
					m_position);
		}

		gotFrame = true;
	}
}

void AudioDec::flush()
{
	AVPacket packet;
	av_init_packet(&packet);
	packet.data = NULL;
	packet.size = 0;
	while (feed(packet));
}

void AudioDec::discontinuity()
{
	if (m_output)
		m_output->onDiscontinuity();
}

double AudioDec::getPosition() const
{
	return m_position;
}

ConnectedAudioOutputs AudioDec::getConnectedOutputs() const
{
	ConnectedAudioOutputs outs;
	if (m_output)
		outs.push_back(ConnectedAudioOutput("", m_output));
	return outs;
}

