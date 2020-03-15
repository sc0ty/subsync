#include "demux.h"
#include "general/scope.h"
#include "general/logger.h"
#include "general/exception.h"

using namespace std;


static AVInputFormat *getInputFormatByFname(const char *path);


#define VALIDATE_STREAM_ID(streamId) \
	if (streamId >= m_streamsNo) \
		throw EXCEPTION("stream ID out of range") \
			.module("Demux") \
			.add("id", streamId) \
			.add("range", m_streamsNo)


Demux::Demux(const string &fileName, function<bool()> runCb) :
	m_formatContext(NULL),
	m_position(0.0),
	m_streams(NULL),
	m_streamsNo(0),
	m_runCb(runCb)
{
	m_formatContext = avformat_alloc_context();
	if (m_formatContext == NULL)
		throw EXCEPTION("can't allocate AVFormatContext")
			.module("Demux", "avformat_alloc_context")
			.file(fileName);

	if (runCb)
	{
		m_formatContext->interrupt_callback.callback = Demux::interruptCallback;
		m_formatContext->interrupt_callback.opaque = this;
	}

	int res = avformat_open_input(&m_formatContext, fileName.c_str(), NULL, NULL);
	if (res < 0 && res != AVERROR_EXIT)
	{
		logger::warn("demux", "avformat_open_input failed, trying to identify file by extension"
				" file \"%s\", error %x: %s", fileName.c_str(), res,
				ffmpegCodeDescription(res).c_str());

		// try to detect container by file extension - works for slightly broken subtitles
		AVInputFormat *fmt = getInputFormatByFname(fileName.c_str());
		if (fmt && avformat_open_input(&m_formatContext, fileName.c_str(), fmt, NULL) == 0)
			res = 0;
	}

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

void Demux::connectDec(shared_ptr<Decoder> dec, unsigned streamId)
{
	VALIDATE_STREAM_ID(streamId);
	m_streams[streamId].connectDecoder(dec);
}

void Demux::disconnectDec(shared_ptr<Decoder> dec, unsigned streamId)
{
	VALIDATE_STREAM_ID(streamId);

	if (!m_streams[streamId].disconnectDecoder(dec))
	{
		throw EXCEPTION("decoder is not connected to this demux")
			.module("Demux");
	}
}

void Demux::disconnectAllDec(shared_ptr<Decoder> dec)
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
		const AVStream *avStream = m_formatContext->streams[i];

		for (shared_ptr<Decoder> dec : m_streams[i].decoders)
			dec->start(avStream);
	}
}

void Demux::stop()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (shared_ptr<Decoder> dec : m_streams[i].decoders)
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
		ScopeExit scopedPacketUnrefGuard([&packet](){ av_packet_unref(&packet); });

		unsigned streamID = packet.stream_index;
		if (streamID < m_streamsNo)
		{
			Demux::Stream &stream = m_streams[streamID];

			for (shared_ptr<Decoder> dec : stream.decoders)
				dec->feed(&packet);

			if (packet.pts != AV_NOPTS_VALUE)
				m_position = (double) packet.pts * stream.timeBase;
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
		for (shared_ptr<Decoder> dec : m_streams[i].decoders)
			dec->discontinuity();
	}
}

void Demux::flush()
{
	for (unsigned i = 0; i < m_streamsNo; i++)
	{
		for (shared_ptr<Decoder> dec : m_streams[i].decoders)
			dec->flush();
	}
}

int Demux::interruptCallback(void *context)
{
	Demux *d = (Demux*) context;
	return d->m_runCb && d->m_runCb() ? 0 : 1;
}


/*** Demux::Stream ***/

Demux::Stream::Stream() : timeBase(0.0)
{}

void Demux::Stream::connectDecoder(shared_ptr<Decoder> decoder)
{
	for (shared_ptr<Decoder> dec : decoders)
	{
		if (dec == decoder)
			throw EXCEPTION("decoder already connected to this stream")
				.module("Demux", "Stream");
	}

	decoders.push_back(decoder);
}

bool Demux::Stream::disconnectDecoder(shared_ptr<Decoder> decoder)
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


/*** Helper functions ***/

AVInputFormat *getInputFormatByFname(const char *path)
{
	const char *p = strrchr(path, '.');
	if (p == NULL)
		return NULL;

	string ext;
	for (p++; *p; p++)
		ext += tolower(*p);

	static const char *formatExtensions[] = {
		"aqt", "aqtitle",
		"ass", "ass",
		"jss", "jacosub",
		"mpl", "mpl2",
		"pjs", "pjs",
		"rt", "realtext",
		"sami", "sami",
		"smi", "sami",
		"srt", "srt",
		"ssa", "ass",
		"stl", "stl",
		"sub", "microdvd",
		"txt", "vplayer",
	};

	AVInputFormat *fmt = NULL;
	for (size_t i = 0; i < sizeof(formatExtensions)/sizeof(const char*); i += 2)
	{
		if (strcmp(ext.c_str(), formatExtensions[i]) == 0)
		{
			const char *name = formatExtensions[i + 1];
			fmt = av_find_input_format(name);
			logger::info("demux", "found format %s by extension for %s", name, path);
			break;
		}
	}

	if (fmt == NULL)
		fmt = av_find_input_format(ext.c_str());

	if (fmt == NULL)
		logger::warn("demux", "couldn't find format by extension for %s", path);

	return fmt;
}
