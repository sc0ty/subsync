#include "audiodmx.h"
#include "general/exception.h"
#include <cstring>
#include <string>

using namespace std;


static const size_t BUFFER_SIZE = 2048;


AudioDemux::AudioDemux() :
	m_sampleSize(0),
	m_channelsNo(0),
	m_buffer(NULL),
	m_channelSize(0),
	m_pos(0),
	m_timestamp(0.0)
{
}

AudioDemux::~AudioDemux()
{
	delete [] m_buffer;
}

void AudioDemux::setOutputFormat(unsigned sampleSize, unsigned channelsNo)
{
	m_sampleSize = sampleSize;
	m_channelsNo = channelsNo;
	m_outputs.resize(m_channelsNo);
	m_channelSize = BUFFER_SIZE * m_sampleSize;

	delete [] m_buffer;
	m_buffer = new uint8_t[m_channelSize * m_channelsNo];
}

void AudioDemux::setOutputFormat(const AudioFormat &format)
{
	setOutputFormat(format.getSampleSize(), format.channelsNo);
}

void AudioDemux::connectOutputChannel(unsigned channelNo, AudioOutput *output)
{
	if (m_channelsNo == 0)
		throw EXCEPTION("output format not set").module("AudioDemux");

	if (channelNo >= m_channelsNo)
		throw EXCEPTION("channel number out of range")
			.module("AudioDemux")
			.add("channel", channelNo)
			.add("max_channel", m_channelsNo - 1);

	m_outputs[channelNo] = output;
}

void AudioDemux::start()
{
	for (AudioOutput *out : m_outputs)
	{
		if (out)
			out->start();
	}
}

void AudioDemux::stop()
{
	for (AudioOutput *out : m_outputs)
	{
		if (out)
			out->stop();
	}
}

void AudioDemux::onNewData(const uint8_t *data, size_t size, double ts)
{
	unsigned ch = 0;

	if (m_pos == 0)
		m_timestamp = ts;

	try
	{
		for (size_t i = 0; i < size; i += m_sampleSize)
		{
			const uint8_t *src = data + i;
			uint8_t *dst = m_buffer + ch*m_channelSize + m_pos;
			memcpy(dst, src, m_sampleSize);

			if (++ch >= m_channelsNo)
			{
				m_pos += m_sampleSize;
				if (m_pos >= m_channelSize)
				{
					for (unsigned ch = 0; ch < m_channelsNo; ch++)
					{
						AudioOutput *out = m_outputs[ch];
						if (out)
							out->onNewData(m_buffer+ch*m_channelSize,
									m_channelSize, m_timestamp);
					}
					m_pos = 0;
					m_timestamp = ts;
				}
				ch = 0;
			}
		}
	}
	catch (...)
	{
		m_pos = 0;
		throw;
	}
}

void AudioDemux::onDiscontinuity()
{
	m_pos = 0;

	for (unsigned ch = 0; ch < m_channelsNo; ch++)
	{
		AudioOutput *output = m_outputs[ch];
		if (output)
			output->onDiscontinuity();
	}
}

ConnectedAudioOutputs AudioDemux::getConnectedOutputs() const
{
	ConnectedAudioOutputs outs;
	for (unsigned ch = 0; ch < m_channelsNo; ch++)
	{
		AudioOutput *output = m_outputs[ch];
		if (output)
			outs.push_back(ConnectedAudioOutput("channel" + to_string(ch), output));
	}
	return outs;
}
