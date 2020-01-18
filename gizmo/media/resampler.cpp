#include "resampler.h"
#include "avout.h"
#include "exception.h"

using namespace std;


Resampler::Resampler() :
	m_output(NULL),
	m_swr(NULL),
	m_outFrame(NULL),
	m_bufferSize(0),
	m_timeBase(0.0)
{
	m_swr = swr_alloc();
}

Resampler::~Resampler()
{
	if (m_swr)
		swr_free(&m_swr);

	if (m_outFrame)
		av_frame_free(&m_outFrame);

	m_bufferSize = 0;
}

void Resampler::connectOutput(shared_ptr<AVOutput> output,
		const AudioFormat &format, int bufferSize)
{
	if (m_outFrame)
		av_frame_free(&m_outFrame);

	m_outFrame = av_frame_alloc();
	m_outFrame->format = format.sampleFormat;
	m_outFrame->channels = format.channelsNo;
	m_outFrame->channel_layout = format.channelLayout;
	m_outFrame->sample_rate = format.sampleRate;
	m_outFrame->nb_samples = bufferSize;

	m_bufferSize = bufferSize;
	int res = av_frame_get_buffer(m_outFrame, 0);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't allocate output audio frame", res)
			.module("Resampler", "av_frame_get_buffer")
			.add("format", format.toString());

	m_output = output;
}

void Resampler::connectFormatChangeCallback(Resampler::FormatChangeCallback cb)
{
	m_formatChangeCb = cb;
}

void Resampler::setChannelMap(const ChannelsMap &channelsMap)
{
	m_channelsMap = channelsMap;
}

void Resampler::start(const AVStream *stream)
{
	m_timeBase = av_q2d(stream->time_base);

	if (m_output)
		m_output->start(stream);
}

void Resampler::stop()
{
	if (m_output)
		m_output->stop();

	swr_close(m_swr);
}

static vector<double> makeMixMap(const AudioFormat &out, const AudioFormat &in,
		Resampler::ChannelsMap channelsMap)
{
	vector<double> mixMap;
	mixMap.resize(in.channelsNo * out.channelsNo);

	for (const auto &ch : channelsMap)
	{
		int i = av_get_channel_layout_channel_index(
				in.channelLayout,
				get<0>(ch.first));

		int o = av_get_channel_layout_channel_index(
				out.channelLayout,
				get<1>(ch.first));

		if (i >= 0 && o >= 0)
			mixMap[i * out.channelsNo + o] = ch.second;
	}

	return mixMap;
}

void Resampler::initSwrContext(const AudioFormat &out, const AudioFormat &in)
{
	if (swr_is_initialized(m_swr))
		swr_close(m_swr);

	m_swr = swr_alloc_set_opts(m_swr,
			out.channelLayout, out.sampleFormat, out.sampleRate,
			in.channelLayout,  in.sampleFormat,  in.sampleRate,
			0, NULL);

	if (m_swr == NULL)
		throw EXCEPTION("can't initialize resampler context")
			.module("Resampler", "swr_alloc_set_opts")
			.add("input", in.toString())
			.add("output", out.toString());

	if (!m_channelsMap.empty())
	{
		vector<double> mixMap = makeMixMap(out, in, m_channelsMap);
		int res = swr_set_matrix(m_swr, mixMap.data(), out.channelsNo);
		if (res < 0)
			throw EXCEPTION_FFMPEG("can't initialize audio mixer", res)
				.module("Resampler", "swr_set_matrix")
				.add("input", in.toString())
				.add("output", out.toString());
	}

	int res = swr_init(m_swr);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't initialize audio resampler", res)
			.module("Resampler", "swr_init")
			.add("input", in.toString())
			.add("output", out.toString());
}

void Resampler::feed(const AVFrame *frame)
{
	m_outFrame->nb_samples = m_bufferSize;
	m_outFrame->pts = frame->pts;

	if (!swr_is_initialized(m_swr))
	{
		if (m_formatChangeCb)
			m_formatChangeCb(AudioFormat(frame), AudioFormat(m_outFrame));

		initSwrContext(m_outFrame, frame);
	}

	int res = swr_convert_frame(m_swr, m_outFrame, frame);
	if (res < 0)
	{
		if (res == AVERROR_INPUT_CHANGED)
		{
			if (m_formatChangeCb)
				m_formatChangeCb(AudioFormat(frame), AudioFormat(m_outFrame));

			swr_close(m_swr);
			initSwrContext(m_outFrame, frame);
			res = swr_convert_frame(m_swr, m_outFrame, frame);
		}

		if (res < 0)
		{
			throw EXCEPTION_FFMPEG("error during audio conversion", res)
				.module("Resampler", "swr_convert")
				.add("input", AudioFormat(frame).toString())
				.add("output", AudioFormat(m_outFrame).toString())
				.add("pts", frame->pts)
				.time(m_timeBase * frame->pts);
		}
	}

	if (m_output)
		m_output->feed(m_outFrame);
}

void Resampler::flush()
{
	if (swr_is_initialized(m_swr))
	{
		while (true)
		{
			m_outFrame->nb_samples = m_bufferSize;
			int res = swr_convert_frame(m_swr, m_outFrame, NULL);

			if (res < 0)
			{
				throw EXCEPTION_FFMPEG("error during audio conversion", res)
					.module("Resampler", "swr_convert")
					.add("output", AudioFormat(m_outFrame).toString())
					.add("pts", m_outFrame->pts)
					.time(m_timeBase * m_outFrame->pts);
			}

			if (m_outFrame->nb_samples <= 0)
				break;

			if (m_output)
				m_output->feed(m_outFrame);
		}
	}
}

void Resampler::discontinuity()
{
	if (m_output)
		m_output->discontinuity();
}

