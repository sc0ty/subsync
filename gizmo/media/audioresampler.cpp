#include "audioresampler.h"
#include "audioout.h"
#include "general/exception.h"

using namespace std;


AudioResampler::AudioResampler() :
	m_output(NULL),
	m_swr(NULL),
	m_buffer(NULL),
	m_bufferSize(0),
	m_inSampleSizeChs(0),
	m_outSampleSizeChs(0)
{
}

AudioResampler::~AudioResampler()
{
	if (m_swr)
		swr_free(&m_swr);

	if (m_buffer)
		av_freep(&m_buffer);

	m_bufferSize = 0;
}

void AudioResampler::connectOutput(AudioOutput *output)
{
	m_output = output;
}

void AudioResampler::setParams(const AudioFormat &in, const AudioFormat &out,
		const vector<double> &mixMap, int bufferSize)
{
	int res;

	m_swr = swr_alloc_set_opts(m_swr,
			out.channelLayout, out.sampleFormat, out.sampleRate,
			in.channelLayout,  in.sampleFormat,  in.sampleRate,
			0, NULL);

	if (m_swr == NULL)
		throw EXCEPTION("can't initialize resampler context")
			.module("AudioResampler", "swr_alloc_set_opts")
			.add("input", in.toString())
			.add("output", out.toString());

	m_inSampleSizeChs = in.getSampleSize() * in.channelsNo;
	m_outSampleSizeChs = out.getSampleSize() * out.channelsNo;

	if (!mixMap.empty())
	{
		res = swr_set_matrix(m_swr, mixMap.data(), out.channelsNo);
		if (res < 0)
			throw EXCEPTION_FFMPEG("can't initialize audio mixer", res)
				.module("AudioResampler", "swr_set_matrix");
	}

	res = swr_init(m_swr);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't initialize audio resampler", res)
			.module("AudioResampler", "swr_init")
			.add("input", in.toString())
			.add("output", out.toString());

	if (m_bufferSize != bufferSize)
	{
		if (m_buffer)
			av_freep(&m_buffer);

		m_bufferSize = bufferSize;
		res = av_samples_alloc(&m_buffer,
				NULL,
				in.channelsNo,
				m_bufferSize,
				out.sampleFormat,
				0);

		if (res < 0)
			throw EXCEPTION_FFMPEG("can't allocate sample buffer", res)
				.module("AudioResampler", "av_samples_alloc")
				.add("channels", in.channelsNo)
				.add("size", m_bufferSize);
	}
}

void AudioResampler::start()
{
	if (m_output)
		m_output->start();
}

void AudioResampler::stop()
{
	if (m_output)
		m_output->stop();
}

void AudioResampler::onNewData(const uint8_t *data, size_t size, double timestamp)
{
	int res = swr_convert(
			m_swr,
			&m_buffer,
			m_bufferSize,
			(const uint8_t**) data,
			size / m_inSampleSizeChs);

	if (res < 0)
		throw EXCEPTION_FFMPEG("error during audio conversion", res)
			.module("AudioResampler", "swr_convert")
			.time(timestamp);

	if (m_output)
		m_output->onNewData(m_buffer, res*m_outSampleSizeChs, timestamp);
}

void AudioResampler::onDiscontinuity()
{
	if (m_output)
		m_output->onDiscontinuity();
}

ConnectedAudioOutputs AudioResampler::getConnectedOutputs() const
{
	ConnectedAudioOutputs outs;
	if (m_output)
		outs.push_back(ConnectedAudioOutput("", m_output));
	return outs;
}
