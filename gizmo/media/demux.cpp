#include "demux.h"
#include "general/exception.h"
#include <memory>
#include <assert.h>

using namespace std;


static void init()
{
	static bool initialized = false;
	if (!initialized)
	{
		av_register_all();
		initialized = true;
	}
}

#define VALIDATE_STREAM_ID(streamId) \
	if (streamId >= m_streamsNo) \
		throw EXCEPTION("stream ID out of range") \
			.module("Demux") \
			.add("id", streamId) \
			.add("range", m_streamsNo)

Demux::Demux(const string &fileName) :
	m_formatContext(NULL),
	m_position(0.0),
	m_streams(NULL),
	m_streamsNo(0)
{
	init();

	int res = avformat_open_input(&m_formatContext, fileName.c_str(), NULL, NULL);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't open multimedia file", res)
			.module("Demux", "avformat_open_input")
			.file(fileName);

	res = avformat_find_stream_info(m_formatContext, NULL);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't read multimedia file", res)
			.module("Demux", "avformat_find_stream_info")
			.file(fileName);

	m_streamsNo = m_formatContext->nb_streams;
	m_streams = new Demux::Stream[m_streamsNo];
	m_streamsInfo.reserve(m_streamsNo);

	for (unsigned i=0; i<m_streamsNo;  i++)
	{
		AVStream *stream = m_formatContext->streams[i];
		StreamFormat info(i, stream);
		m_streamsInfo.push_back(info);

		m_streams[i].timeBase =
			(double)stream->time_base.num / (double)stream->time_base.den;
	}
}

Demux::~Demux()
{
	delete [] m_streams;
	m_streams = NULL;
	avformat_close_input(&m_formatContext);
}

const StreamsFormat &Demux::getStreamsInfo() const
{
	return m_streamsInfo;
}

AVStream *Demux::getStreamRawData(unsigned streamId) const
{
	VALIDATE_STREAM_ID(streamId);
	return m_formatContext->streams[streamId];
}

void Demux::connectDec(Decoder *dec, unsigned streamId)
{
	VALIDATE_STREAM_ID(streamId);
	m_streams[streamId].connectDecoder(dec);
}

void Demux::disconnectDec(Decoder *dec, unsigned streamId)
{
	VALIDATE_STREAM_ID(streamId);

	if (!m_streams[streamId].disconnectDecoder(dec))
	{
		throw EXCEPTION("decoder is not connected to this demux")
			.module("Demux");
	}
}

void Demux::disconnectAllDec(Decoder *dec)
{
	bool disconnected = false;

	for (unsigned i = 0; i < m_streamsNo; i++)
		disconnected |= m_streams[i].disconnectDecoder(dec);

	if (!disconnected)
		throw EXCEPTION("decoder is not connected to this demux")
			.module("Demux");
}

void Demux::start()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (Decoder *dec : m_streams[i].decoders)
			dec->start();
	}
}

void Demux::stop()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (Decoder *dec : m_streams[i].decoders)
			dec->stop();
	}
}

bool Demux::step()
{
	AVPacket packet;
	av_init_packet(&packet);

	int res = av_read_frame(m_formatContext, &packet);

	if (res >= 0)
	{
		unique_ptr<AVPacket, void(*)(AVPacket*)>
			scopedPacketUnrefGuard(&packet, &av_packet_unref);

		unsigned streamID = packet.stream_index;
		if (streamID < m_streamsNo)
		{
			Demux::Stream &stream = m_streams[streamID];

			for (Decoder *dec : stream.decoders)
				dec->feed(packet);

			m_position = (double)packet.pts * stream.timeBase;
		}

		return true;
	}
	else if (res == AVERROR_EOF)
	{
		flush();
		notifyDiscontinuity();
		return false;
	}
	else
	{
		throw EXCEPTION_FFMPEG("can't read input stream", res)
			.module("Demux", "av_read_frame");
	}
}

double Demux::getPosition() const
{
	return m_position;
}

double Demux::getDuration() const
{
	if (m_formatContext && (m_formatContext->duration > 0))
		return (double)m_formatContext->duration / (double)AV_TIME_BASE;
	else
		return 0.0;
}

void Demux::seek(double timestamp)
{
	int64_t ts = timestamp * AV_TIME_BASE;
	int res = av_seek_frame(m_formatContext, -1, ts, 0);
	if (res < 0)
		throw EXCEPTION_FFMPEG("can't seek", res)
			.module("Demux", "av_seek_frame")
			.time(timestamp);

	m_position = timestamp;
}

void Demux::notifyDiscontinuity()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (Decoder *dec : m_streams[i].decoders)
			dec->discontinuity();
	}
}

void Demux::flush()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (Decoder *dec : m_streams[i].decoders)
			dec->flush();
	}
}

Demux::ConnectedOutputs Demux::getConnectedOutputs() const
{
	ConnectedOutputs res;
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (Decoder *dec : m_streams[i].decoders)
		{
			res.push_back(ConnectedOutput("stream" + to_string(i), dec));
		}
	}
	return res;
}

/*** Demux::Stream ***/

Demux::Stream::Stream() : timeBase(0.0)
{}

void Demux::Stream::connectDecoder(Decoder *decoder)
{
	for (Decoder *dec : decoders)
	{
		if (dec == decoder)
			throw EXCEPTION("decoder already connected to this stream")
				.module("Demux", "Stream");
	}

	decoders.push_back(decoder);
}

bool Demux::Stream::disconnectDecoder(Decoder *decoder)
{
	for (Decoders::iterator it = decoders.begin(); it != decoders.end(); ++it)
	{
		if (*it == decoder)
		{
			decoders.erase(it);
			return true;
		}
	}

	return false;
}
