#include "exception.h"

extern "C"
{
#include <libavutil/error.h>
#include <libavcodec/avcodec.h>
}

using namespace std;


FFmpegException::FFmpegException(const std::string &msg, int errnum) throw()
	: Exception(msg, codeDescription(errnum))
{
	averror(errnum);
}

FFmpegException::~FFmpegException() throw()
{}

FFmpegException &FFmpegException::averror(int errnum) throw()
{
	code(errnum);
	const string name = codeName(errnum);
	if (!name.empty())
		add("averror", name);
	return *this;
}

string FFmpegException::codeDescription(int code) throw()
{
	string res;
	switch (code)
	{
		case AVERROR_BUG:
		case AVERROR_BUG2:
			res = "internal error";
			break;

		case AVERROR_BUFFER_TOO_SMALL:
			res = "buffer too small";
			break;

		case AVERROR_DECODER_NOT_FOUND:
			res = "decoder not found";
			break;

		case AVERROR_DEMUXER_NOT_FOUND:
			res = "demuxer not found";
			break;

		case AVERROR_ENCODER_NOT_FOUND:
			res = "encoder not found";
			break;

		case AVERROR_EOF:
			res = "eof";
			break;

		case AVERROR_FILTER_NOT_FOUND:
			res = "filter not found";
			break;

		case AVERROR_INVALIDDATA:
			res = "invalid data";
			break;

		case AVERROR_MUXER_NOT_FOUND:
			res = "muxer not found";
			break;

		case AVERROR_OPTION_NOT_FOUND:
			res = "option not found";
			break;

		case AVERROR_PROTOCOL_NOT_FOUND:
			res = "protocol not found";
			break;

		case AVERROR_STREAM_NOT_FOUND:
			res = "stream not found";
			break;
	}

	char buffer[1024];
	if (av_strerror(code, buffer, sizeof(buffer)) == 0)
	{
		if (!res.empty())
			res += ": ";
		res += buffer;
	}

	return res;
}

string FFmpegException::codeName(int code) throw()
{
	switch (code)
	{
		case AVERROR_BSF_NOT_FOUND: return "AVERROR_BSF_NOT_FOUND";
		case AVERROR_BUG: return "AVERROR_BUG";
		case AVERROR_BUFFER_TOO_SMALL: return "AVERROR_BUFFER_TOO_SMALL";
		case AVERROR_DECODER_NOT_FOUND: return "AVERROR_DECODER_NOT_FOUND";
		case AVERROR_DEMUXER_NOT_FOUND: return "AVERROR_DEMUXER_NOT_FOUND";
		case AVERROR_ENCODER_NOT_FOUND: return "AVERROR_ENCODER_NOT_FOUND";
		case AVERROR_EOF: return "AVERROR_EOF";
		case AVERROR_EXIT: return "AVERROR_EXIT";
		case AVERROR_EXTERNAL: return "AVERROR_EXTERNAL";
		case AVERROR_FILTER_NOT_FOUND: return "AVERROR_FILTER_NOT_FOUND";
		case AVERROR_INVALIDDATA: return "AVERROR_INVALIDDATA";
		case AVERROR_MUXER_NOT_FOUND: return "AVERROR_MUXER_NOT_FOUND";
		case AVERROR_OPTION_NOT_FOUND: return "AVERROR_OPTION_NOT_FOUND";
		case AVERROR_PATCHWELCOME: return "AVERROR_PATCHWELCOME";
		case AVERROR_PROTOCOL_NOT_FOUND: return "AVERROR_PROTOCOL_NOT_FOUND";
		case AVERROR_STREAM_NOT_FOUND: return "AVERROR_STREAM_NOT_FOUND";
		case AVERROR_BUG2: return "AVERROR_BUG2";
		case AVERROR_UNKNOWN: return "AVERROR_UNKNOWN";
		case AVERROR_EXPERIMENTAL: return "AVERROR_EXPERIMENTAL";
		case AVERROR_INPUT_CHANGED: return "AVERROR_INPUT_CHANGED";
		case AVERROR_OUTPUT_CHANGED: return "AVERROR_OUTPUT_CHANGED";
		case AVERROR_HTTP_BAD_REQUEST: return "AVERROR_HTTP_BAD_REQUEST";
		case AVERROR_HTTP_UNAUTHORIZED: return "AVERROR_HTTP_UNAUTHORIZED";
		case AVERROR_HTTP_FORBIDDEN: return "AVERROR_HTTP_FORBIDDEN";
		case AVERROR_HTTP_NOT_FOUND: return "AVERROR_HTTP_NOT_FOUND";
		case AVERROR_HTTP_OTHER_4XX: return "AVERROR_HTTP_OTHER_4XX";
		case AVERROR_HTTP_SERVER_ERROR: return "AVERROR_HTTP_SERVER_ERROR";
		default: return "";
	}
}
